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

};