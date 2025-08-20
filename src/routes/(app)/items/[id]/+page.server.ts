import type { Actions, PageServerLoad } from './$types';
import { fail, redirect } from '@sveltejs/kit';
import prisma from '$lib/server/prisma';

export const load: PageServerLoad = async ({ locals, params, url }) => {
    if (!locals.user) {
        throw redirect(303, `/login?redirectTo=${url.pathname}`);
    }

    const item = await prisma.item.findUnique({
        where: { id: parseInt(params.id) },
    });
    if (!item) {
        throw fail(404, { error: "Item not found." });
    }

    const categories = await prisma.category.findMany();
    if (!categories) {
        throw fail(404, { error: "No categories found." });
    }

    return { item, categories };
};


export const actions: Actions = {
    edit: async ({ request, locals, params }) => {
        if (!locals.user) {
            return fail(401, { error: 'You must be logged in to edit an item.' });
        }

        const form = await request.formData();

        // NAME
        const itemName = form.get('name')?.toString();
        if (!itemName) {
            return fail(400, { error: 'Item name is missing.' });
        }

        // QUANTITY
        const itemQuantityStr = form.get('quantity')?.toString();
        let itemQuantity: number | undefined;
        if (itemQuantityStr && itemQuantityStr.trim() !== '') {
            if (isNaN(Number(itemQuantityStr))) {
                return fail(400, { error: 'Quantity must be a number.' });
            }
            itemQuantity = parseInt(itemQuantityStr, 10);
        }

        // UNIT
        const itemUnit = form.get('unit')?.toString();
        if (!itemUnit) {
            return fail(400, { error: 'Item unit is missing.' });
        }

        // CATEGORY
        const itemCategoryStr = form.get('category')?.toString() ?? "";
        let itemCategoryId: number | null = null;
        if (itemCategoryStr.trim() !== "") {
            itemCategoryId = parseInt(itemCategoryStr, 10);
            const category = await prisma.category.findUnique({
                where: { id: itemCategoryId }
            });
            if (!category) {
                return fail(400, { error: 'Category does not exist.' });
            }
        }

        // NOTES
        const itemNotes = form.get('notes')?.toString() ?? "";

        const updatedItem = await prisma.item.update({
            where: { id: parseInt(params.id) },
            data: {
                name: itemName,
                category_id: itemCategoryId,
                quantity: itemQuantity,
                unit: itemUnit,
                notes: itemNotes,
            }
        });

        return { success: true, message: `${updatedItem.name} updated successfully.` };
    },

    delete: async ({ locals, params }) => {
        if (!locals.user) {
            return fail(401, { error: 'You must be logged in to delete an item.' });
        }

        try {
            await prisma.item.delete({
                where: { id: parseInt(params.id) },
            });
            return { success: true, message: `Item deleted successfully.` };
        } catch (err) {
            return fail(500, { error: 'Failed to delete item.' });
        }
    }
};
