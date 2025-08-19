import type { Actions, PageServerLoad } from './$types';
import { fail, redirect } from '@sveltejs/kit';
import prisma from '$lib/server/prisma';

export const load: PageServerLoad = async ({ locals, url }) => {
    if (!locals.user) {
        throw redirect(303, `/login?redirectTo=${url.pathname}`);
    }
    // Always fetch categories sorted by their intended order
    const categories = await prisma.category.findMany({
        orderBy: { order: 'asc' }
    });
    // The original fail condition was on !categories, but findMany returns an array,
    // so it will never be falsy. An empty array is a valid state.
    return { categories };
};

/**
 * Re-indexes all categories to ensure their 'order' field is a successive sequence (1, 2, 3, ...).
 * This should be called after a category is deleted.
 */
async function reorderCategories() {
    // 1. Fetch all categories, sorted by their current order.
    const categories = await prisma.category.findMany({
        orderBy: { order: 'asc' }
    });

    // 2. Create an array of update promises.
    // Each category's new order is its index in the sorted array + 1.
    const updatePromises = categories.map((category, index) =>
        prisma.category.update({
            where: { id: category.id },
            data: { order: index + 1 }
        })
    );

    // 3. Execute all updates in a single transaction for efficiency and data integrity.
    await prisma.$transaction(updatePromises);
}

export const actions: Actions = {
    create: async ({ request, locals }) => {
        if (!locals.user) {
            return fail(401, { error: 'You must be logged in to add a category.' });
        }
        const form = await request.formData();
        const categoryName = form.get('input-name')?.toString();
        if (!categoryName) {
            return fail(400, { error: 'Category name is missing.' });
        }

        const existingCategory = await prisma.category.findUnique({
            where: { name: categoryName }
        });
        if (existingCategory) {
            return fail(400, { error: 'Category already exists.' });
        }

        // The order for the new category will be the total count + 1.
        // This assumes all other categories are already ordered successively.
        const categoryCount = await prisma.category.count();
        const order = categoryCount + 1;

        await prisma.category.create({
            data: { name: categoryName, order: order }
        });

        const categories = await prisma.category.findMany();
        return { success: true, categories: categories }
    },

    delete: async ({ request, locals }) => {
        if (!locals.user) {
            return fail(401, { error: 'You must be logged in to delete a category.' });
        }
        const form = await request.formData();
        const categoryIdString = form.get('id')?.toString(); // It's better to delete by a unique, non-changing ID.
        if (!categoryIdString) {
            return fail(400, { error: 'Category ID is missing.' });
        }
        const categoryId = parseInt(categoryIdString, 10);
        if (isNaN(categoryId)) {
            return fail(400, { error: 'Invalid category ID.' });
        }

        const category = await prisma.category.findUnique({
            where: { id: categoryId }
        });
        if (!category) {
            return fail(404, { error: 'Category not found.' });
        }

        // Disassociate items before deleting the category
        await prisma.item.updateMany({
            where: { category_id: category.id },
            data: { category_id: null }
        });

        // Now delete the category
        await prisma.category.delete({
            where: { id: categoryId }
        });

        // CRITICAL STEP: Re-order all remaining categories to fill the gap.
        await reorderCategories();

        const categories = await prisma.category.findMany();
        return { success: true, categories: categories }
    },

    rename: async ({ request, locals }) => {
        if (!locals.user) return fail(401, { error: 'You must be logged in to edit a category.' });

        const form = await request.formData();
        const categoryIdString = form.get('id')?.toString();
        const newName = form.get('new-name')?.toString();

        if (!categoryIdString || !newName) {
            return fail(400, { error: 'Missing category ID or new name.' });
        }
        const categoryId = parseInt(categoryIdString, 10);
        if (isNaN(categoryId)) {
            return fail(400, { error: 'Invalid category ID.' });
        }

        // Check if the new name is already in use by another category
        const duplicate = await prisma.category.findFirst({
            where: {
                name: newName,
                id: { not: categoryId } // Exclude the current category from the check
            }
        });
        if (duplicate) {
            return fail(400, { error: 'New name already in use.' });
        }

        await prisma.category.update({
            where: { id: categoryId },
            data: { name: newName }
        });
        const categories = await prisma.category.findMany();
        return { success: true, categories: categories }
    }
};