import type { Actions, PageServerLoad } from './$types';
import { fail, redirect } from '@sveltejs/kit';
import prisma from '$lib/server/prisma';

export const load: PageServerLoad = async ({ locals, url, depends }) => {
    if (!locals.user) {
        throw redirect(303, `/login?redirectTo=${url.pathname}`);
    }
    depends('app:items');

    const items = await prisma.item.findMany({});
    const categories = await prisma.category.findMany();
    return { items, categories };
};


export const actions: Actions = {
    toggle: async ({ request, locals }) => {
        if (!locals.user) {
            return fail(401, { error: "You must be logged in to toggle an item." });
        }

        const form = await request.formData();
        const itemIdString = form.get("id")?.toString();
        if (!itemIdString) {
            return fail(400, { error: "Item ID is missing for toggling." });
        }
        const itemId = parseInt(itemIdString);
        if (isNaN(itemId)) {
            return fail(400, { error: "Invalid Item ID for toggling." });
        }
        const item = await prisma.item.findUnique({
            where: { id: itemId },
        });
        if (!item) {
            return fail(404, { error: "Item not found." });
        }
        const updatedItem = await prisma.item.update({
            where: { id: itemId },
            data: { is_active: !item.is_active },
        });
        return { success: true, item: updatedItem };
    }
};