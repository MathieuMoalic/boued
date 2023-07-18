// store.ts
import { writable } from 'svelte/store';

interface Items {
    Groceries: Array<string>;
    Alcohol: Array<string>;
}

export let items = writable<Items>({ Groceries: [], Alcohol: [] });
export let category = writable<string>("Groceries");
export let matches = writable<string[]>([]);
export let loadingItems = writable<string[]>([]);
export const api = writable<URL>(new URL('./api', window.location.href));

