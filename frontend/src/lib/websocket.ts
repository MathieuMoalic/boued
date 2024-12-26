type WebSocketEventHandler = (data: any) => void;

class WebSocketClient {
    private socket: WebSocket | null = null;
    private url: string;
    private onMessageHandler: WebSocketEventHandler | null = null;
    private onErrorHandler: WebSocketEventHandler | null = null;
    private onOpenHandler: WebSocketEventHandler | null = null;
    private onCloseHandler: WebSocketEventHandler | null = null;

    constructor(url: string) {
        this.url = url;
    }

    connect(): void {
        if (this.socket) {
            console.warn("WebSocket is already connected.");
            return;
        }

        this.socket = new WebSocket(this.url);

        this.socket.addEventListener("open", (event) => {
            this.onOpenHandler && this.onOpenHandler(event);
        });

        this.socket.addEventListener("message", (event) => {
            const data = JSON.parse(event.data);
            this.onMessageHandler && this.onMessageHandler(data);
        });

        this.socket.addEventListener("error", (event) => {
            console.error("WebSocket error:", event);
            this.onErrorHandler && this.onErrorHandler(event);
        });

        this.socket.addEventListener("close", (event) => {
            this.onCloseHandler && this.onCloseHandler(event);
            this.socket = null; // Reset the socket
        });
    }

    disconnect(): void {
        if (!this.socket) {
            console.warn("WebSocket is not connected.");
            return;
        }
        this.socket.close();
    }

    /**
     * Sends a message to the WebSocket server.
     * Waits for the WebSocket to be ready before sending.
     * @param message The message object to send.
     */
    send(message: any): void {
        this.waitForOpenConnection()
            .then(() => {
                this.socket?.send(JSON.stringify(message));
            })
            .catch((error) => {
                console.error("Failed to send message:", error);
            });
    }

    /**
     * Waits for the WebSocket connection to be open.
     * Resolves immediately if the connection is already open.
     * @returns A promise that resolves when the WebSocket is open.
     */
    private waitForOpenConnection(): Promise<void> {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            return Promise.resolve();
        }

        return new Promise((resolve, reject) => {
            const maxRetries = 10;
            const interval = 200; // 200ms

            let retries = 0;

            const checkConnection = () => {
                if (this.socket && this.socket.readyState === WebSocket.OPEN) {
                    resolve();
                } else if (retries >= maxRetries) {
                    reject(new Error("WebSocket connection timed out."));
                } else {
                    retries++;
                    setTimeout(checkConnection, interval);
                }
            };

            checkConnection();
        });
    }

    /**
     * Sets the handler for incoming messages.
     * @param handler The function to handle messages.
     */
    onMessage(handler: WebSocketEventHandler): void {
        this.onMessageHandler = handler;
    }

    /**`
     * Sets the handler for errors.
     * @param handler The function to handle errors.
     */
    onError(handler: WebSocketEventHandler): void {
        this.onErrorHandler = handler;
    }

    /**
     * Sets the handler for connection open events.
     * @param handler The function to handle connection open events.
     */
    onOpen(handler: WebSocketEventHandler): void {
        this.onOpenHandler = handler;
    }

    /**
     * Sets the handler for connection close events.
     * @param handler The function to handle connection close events.
     */
    onClose(handler: WebSocketEventHandler): void {
        this.onCloseHandler = handler;
    }
}

export default WebSocketClient;
