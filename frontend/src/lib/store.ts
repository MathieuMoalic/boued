import { writable } from 'svelte/store';
import WebSocketCRUD from './crud';

export const ws = writable<WebSocketCRUD>(new WebSocketCRUD("ws://127.0.0.1:6001/ws"));
export const tab = writable("Active");