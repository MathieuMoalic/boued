import WebSocketClient from "./websocket";
import { type Item } from "./types";

class WebSocketCRUD {
    private wsClient: WebSocketClient;

    constructor(url: string) {
        this.wsClient = new WebSocketClient(url);
        this.wsClient.connect();
    }

    /**
     * Create an item.
     * @param item The item to create.
     * @returns A promise that resolves with the server's response.
     */
    async createItem(item: Item): Promise<any> {
        return this.sendAction("create", item);
    }

    /**
     * Read all items.
     * @returns A promise that resolves with the list of items.
     */
    async readAllItems(): Promise<Item[]> {
        return this.sendAction("read_all");
    }

    /**
     * Read a single item by ID.
     * @param id The ID of the item to read.
     * @returns A promise that resolves with the item.
     */
    async readItem(id: number): Promise<Item> {
        return this.sendAction("read_one", { id });
    }

    /**
     * Update an item.
     * @param id The ID of the item to update.
     * @param data The data to update the item with.
     * @returns A promise that resolves with the updated item.
     */
    async updateItem(id: number, data: Partial<Item>): Promise<Item> {
        return this.sendAction("update", { id, data });
    }

    /**
     * Delete an item.
     * @param id The ID of the item to delete.
     * @returns A promise that resolves with the deleted item.
     */
    async deleteItem(id: number): Promise<Item> {
        return this.sendAction("delete", { id });
    }

    /**
     * Search items.
     * @param query The search query.
     * @param limit The maximum number of results to return.
     * @returns A promise that resolves with the search results.
     */
    async searchItems(query: string, limit: number = 10): Promise<Item[]> {
        return this.sendAction("search", { query, limit });
    }

    /**
     * Sends an action to the WebSocket and waits for the response.
     * @param action The action to perform.
     * @param payload The payload to send with the action.
     * @returns A promise that resolves with the server's response.
     */
    private sendAction(action: string, payload?: any): Promise<any> {
        return new Promise((resolve, reject) => {
            const message = { action, payload };

            // Handle WebSocket responses
            const handleResponse = (data: any) => {
                if (data.status === "success") {
                    resolve(data.data); // or resolve the entire data object, if desired
                    this.wsClient.onMessage(() => { }); // clear the handler
                }
            };
            4

            this.wsClient.onMessage(handleResponse);

            try {
                this.wsClient.send(message);
            } catch (error) {
                reject(error);
            }
        });
    }
}

export default WebSocketCRUD;
