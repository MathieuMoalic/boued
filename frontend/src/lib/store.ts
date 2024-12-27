import WebSocketCRUD from '$lib/crud';
import { writable, derived } from "svelte/store";
import Fuse from "fuse.js";
import type { Item } from "$lib/types";

export const ws = writable<WebSocketCRUD>(new WebSocketCRUD("/ws"));
export const items = writable<Item[]>([]);
export const searchTerm = writable<string>("");

export const searching = derived(searchTerm, ($searchTerm) => $searchTerm.length > 0);

export const fuse = derived(items, ($items) => {
    return new Fuse($items, {
        keys: ["name"],
        threshold: 0.8,
    });
});

export const searchResults = derived(
    [fuse, searchTerm],
    ([$fuse, $searchTerm]) => {
        if (!$searchTerm) return [];
        return $fuse.search($searchTerm).map((result) => result.item);
    }
);
