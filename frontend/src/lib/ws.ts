import { categories, items } from "./store";

let ws: WebSocket;
let reconnectAttempts = 0;
const maxReconnectAttempts = 10;
const baseReconnectDelay = 1000; // 1 second

interface WebSocketMessage {
    action: "create" | "update" | "delete" | "reorder";
    type: "item" | "category";
    data: any;
}


export const connectWebSocket = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
        return;
    }

    ws = new WebSocket("/ws");

    ws.addEventListener("open", () => {
        console.log("WebSocket connection established");
        reconnectAttempts = 0; // Reset on successful connection
    });

    ws.addEventListener("message", (event) => {
        handleMessages(event.data);
    });

    ws.addEventListener("close", () => {
        console.log("WebSocket connection closed, attempting to reconnect...");
        attemptReconnect();
    });

    ws.addEventListener("error", (error) => {
        console.error("WebSocket error:", error);
        ws?.close();
    });
};

const attemptReconnect = () => {
    if (reconnectAttempts < maxReconnectAttempts) {
        const delay = Math.min(baseReconnectDelay * 2 ** reconnectAttempts, 30000); // Max delay of 30 sec
        reconnectAttempts++;
        setTimeout(() => {
            console.log(`Reconnecting... Attempt ${reconnectAttempts}`);
            connectWebSocket();
        }, delay);
    } else {
        console.warn("Max reconnect attempts reached. Stopping retries.");
    }
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
                return [...currentData, data];
            case "update":
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

// Ensure the WebSocket reconnects when the app comes back from background
document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible") {
        console.log("App resumed, checking WebSocket connection...");
        connectWebSocket();
    }
});
