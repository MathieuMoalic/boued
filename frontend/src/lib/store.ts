import { writable } from 'svelte/store';
import WebSocketCRUD from './crud';
import type { Item } from './types';

export const ws = writable<WebSocketCRUD>(new WebSocketCRUD("/ws"));
export const tab = writable("Active");
export const searchQuery = writable("");
export const items = writable<Item[]>([]);
export const searching = writable(false);
export const searchResults = writable<Item[]>([]);