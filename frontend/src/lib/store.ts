// store.ts
import { writable } from 'svelte/store';
import WebSocketCRUD from './crud';

export let ws = writable<WebSocketCRUD>(new WebSocketCRUD("ws://127.0.0.1:6001/ws"));

interface Items {
    Groceries: Array<string>;
    Alcohol: Array<string>;
}

export let items = writable<Items>({ Groceries: [], Alcohol: [] });
export let category = writable<string>("Groceries");
export let matches = writable<string[]>([]);
export let loadingItems = writable<string[]>([]);
export const api = writable<URL>(new URL('./api', window.location.href));

