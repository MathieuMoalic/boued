import { writable } from 'svelte/store';
import WebSocketCRUD from './crud';

export const ws = writable<WebSocketCRUD>(new WebSocketCRUD("/ws"));
export const tab = writable("Active");