import type { Actions, PageServerLoad } from './$types';
import { fail, redirect } from '@sveltejs/kit';
import prisma from '$lib/server/prisma';

export const load: PageServerLoad = async ({ locals, url }) => {
    if (!locals.user) {
        throw redirect(303, `/login?redirectTo=${url.pathname}`);
    }
    const categories = await prisma.category.findMany({
        orderBy: { order: 'asc' }
    });
    return { categories };
};


// Put this near your other helpers
async function reorderCategoriesSafe() {
    await prisma.$transaction(async (tx) => {
        // Get categories in a stable order
        const categories = await tx.category.findMany({
            orderBy: [{ order: 'asc' }, { id: 'asc' }],
            select: { id: true }
        });

        if (categories.length === 0) return;

        const { _max } = await tx.category.aggregate({ _max: { order: true } });
        const base = (_max.order ?? 0) + 1; // guaranteed free range start

        // Phase 1: move everything into a disjoint temp range (all unique)
        for (let i = 0; i < categories.length; i++) {
            await tx.category.update({
                where: { id: categories[i].id },
                data: { order: base + i }
            });
        }

        // Phase 2: renumber 1..n (final positions)
        for (let i = 0; i < categories.length; i++) {
            await tx.category.update({
                where: { id: categories[i].id },
                data: { order: i + 1 }
            });
        }
    });
}

async function reorderCategories() {
    const categories = await prisma.category.findMany({
        orderBy: { order: 'asc' }
    });

    const updatePromises = categories.map((category, index) =>
        prisma.category.update({
            where: { id: category.id },
            data: { order: index + 1 }
        })
    );

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
        const categoryIdString = form.get('id')?.toString();
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

        await prisma.item.updateMany({
            where: { category_id: category.id },
            data: { category_id: null }
        });

        await prisma.category.delete({
            where: { id: categoryId }
        });

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

        const duplicate = await prisma.category.findFirst({
            where: {
                name: newName,
                id: { not: categoryId }
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
    },

    moveup: async ({ request, locals }) => {
        if (!locals.user) {
            return fail(401, { error: 'You must be logged in to move a category.' });
        }
        const form = await request.formData();
        const categoryIdString = form.get('id')?.toString();
        if (!categoryIdString) {
            return fail(400, { error: 'Category ID is missing.' });
        }
        const categoryId = parseInt(categoryIdString, 10);
        if (isNaN(categoryId)) {
            return fail(400, { error: 'Invalid category ID.' });
        }

        const category = await prisma.category.findUnique({ where: { id: categoryId } });
        if (!category) return fail(404, { error: 'Category not found.' });

        const previousCategory = await prisma.category.findFirst({
            where: { order: category.order - 1 }
        });
        if (!previousCategory) {
            const categories = await prisma.category.findMany({ orderBy: { order: 'asc' } });
            return { success: true, categories }; // already at top
        }

        await prisma.$transaction(async (tx) => {
            const { _max } = await tx.category.aggregate({ _max: { order: true } });
            const temp = (_max.order ?? 0) + 1;

            // Move current to a free temp slot, then swap
            await tx.category.update({ where: { id: category.id }, data: { order: temp } });
            await tx.category.update({
                where: { id: previousCategory.id },
                data: { order: category.order }
            });
            await tx.category.update({
                where: { id: category.id },
                data: { order: previousCategory.order }
            });
        });

        // no need to reindex, but it doesn't hurt to keep things tight:
        await reorderCategoriesSafe();

        const categories = await prisma.category.findMany({ orderBy: { order: 'asc' } });
        return { success: true, categories };
    },

    movedown: async ({ request, locals }) => {
        if (!locals.user) {
            return fail(401, { error: 'You must be logged in to move a category.' });
        }
        const form = await request.formData();
        const categoryIdString = form.get('id')?.toString();
        if (!categoryIdString) {
            return fail(400, { error: 'Category ID is missing.' });
        }
        const categoryId = parseInt(categoryIdString, 10);
        if (isNaN(categoryId)) {
            return fail(400, { error: 'Invalid category ID.' });
        }

        // inside actions.movedown (mirror of moveup)
        const category = await prisma.category.findUnique({ where: { id: categoryId } });
        if (!category) return fail(404, { error: 'Category not found.' });

        const nextCategory = await prisma.category.findFirst({
            where: { order: category.order + 1 }
        });
        if (!nextCategory) {
            const categories = await prisma.category.findMany({ orderBy: { order: 'asc' } });
            return { success: true, categories }; // already at bottom
        }

        await prisma.$transaction(async (tx) => {
            const { _max } = await tx.category.aggregate({ _max: { order: true } });
            const temp = (_max.order ?? 0) + 1;

            await tx.category.update({ where: { id: category.id }, data: { order: temp } });
            await tx.category.update({
                where: { id: nextCategory.id },
                data: { order: category.order }
            });
            await tx.category.update({
                where: { id: category.id },
                data: { order: nextCategory.order }
            });
        });

        await reorderCategoriesSafe();

        const categories = await prisma.category.findMany({ orderBy: { order: 'asc' } });
        return { success: true, categories };
    }
};