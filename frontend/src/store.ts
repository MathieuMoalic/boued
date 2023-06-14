// store.ts
import MeiliSearch from 'meilisearch';
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
export let meili_client = writable<MeiliSearch>(new MeiliSearch({
    host: origin + "/search",
    apiKey: "3982r7t5gruef09248g379ruocnije802g97yiv",
}))
