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

};