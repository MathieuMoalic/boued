import type { Actions, PageServerLoad } from './$types';
import { fail, redirect } from '@sveltejs/kit';
import prisma from '$lib/server/prisma';

export const load: PageServerLoad = async ({ locals, url }) => {
    if (!locals.user) {
        throw redirect(303, `/login?redirectTo=${url.pathname}`);
    }
    const categories = await prisma.category.findMany();
    if (!categories) {
        throw fail(404, { error: "No categories found." });
    }
    return { categories };
};


export const actions: Actions = {
    create: async ({ request, locals }) => {
        if (!locals.user) {
            return fail(401, { error: 'You must be logged in to add an item.' });
        }
        const form = await request.formData();

        // NAME
        const itemName = form.get('name')?.toString();
        if (!itemName) {
            return fail(400, { error: 'Item name is missing.' });
        }
        const existingItem = await prisma.item.findUnique({
            where: { name: itemName }
        });
        if (existingItem) {
            return fail(400, { error: 'Item already exists.' });
        }

        // QUANTITY
        const itemQuantityStr = form.get('quantity')?.toString();
        let itemQuantity: number | undefined;
        if (itemQuantityStr !== undefined && itemQuantityStr !== null && itemQuantityStr.trim() !== '') {
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


        const item = await prisma.item.create({
            data: {
                name: itemName,
                category_id: itemCategoryId,
                quantity: itemQuantity,
                unit: itemUnit,
            }
        });
        return { success: true, message: `${item.name} created successfully.` };
    },
};