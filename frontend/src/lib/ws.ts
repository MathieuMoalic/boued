import { addAlert } from "./alert";
import { categories, items } from "./store";

let ws: WebSocket;

interface WebSocketMessage {
    action: "create" | "update" | "delete" | "reorder";
    type: "item" | "category";
    data: any;
}


export const connectWebSocket = () => {
    ws = new WebSocket("/ws");

    ws.addEventListener("open", () => {
        console.log("WebSocket connection established");
    });

    ws.addEventListener("message", (event) => {
        handleMessages(event.data);
    });

    ws.addEventListener("close", () => {
        console.log("WebSocket connection closed");
    });

    ws.addEventListener("error", (error) => {
        console.error("WebSocket error:", error);
    });
};

function handleMessages(data: any) {
    const msg: WebSocketMessage = JSON.parse(data);

    const handlers: Record<string, (data: any) => void> = {
        "item": (data) => handleUpdate(items, data, msg.action),
        "category": (data) => handleUpdate(categories, data, msg.action),
    };

    if (handlers[msg.type]) {
        handlers[msg.type](msg.data);
    } else {
        console.warn(`Unhandled type: ${msg.type}`);
    }
}

function handleUpdate(store: any, data: any, action: string) {
    store.update((currentData: any[]) => {
        switch (action) {
            case "create":
                console.log("create", data);
                return [...currentData, data];
            case "update":
                // addAlert(`${item.name} updated`, "success");
                return currentData.map((item) =>
                    item.id === data.id ? { ...item, ...data } : item
                );
            case "delete":
                return currentData.filter((item) => item.id !== data.id);
            case "reorder":
                return data;
            default:
                console.warn(`Unhandled action: ${action}`);
                return currentData;
        }
    });
}
