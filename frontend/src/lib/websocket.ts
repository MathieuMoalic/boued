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

    /**
     * Connects to the WebSocket server.
     */
    connect(): void {
        if (this.socket) {
            console.warn("WebSocket is already connected.");
            return;
        }

        this.socket = new WebSocket(this.url);

        this.socket.addEventListener("open", (event) => {
            console.log("WebSocket connection established.");
            this.onOpenHandler && this.onOpenHandler(event);
        });

        this.socket.addEventListener("message", (event) => {
            const data = JSON.parse(event.data);
            console.log("WebSocket message received:", data);
            this.onMessageHandler && this.onMessageHandler(data);
        });

        this.socket.addEventListener("error", (event) => {
            console.error("WebSocket error:", event);
            this.onErrorHandler && this.onErrorHandler(event);
        });

        this.socket.addEventListener("close", (event) => {
            console.log("WebSocket connection closed.");
            this.onCloseHandler && this.onCloseHandler(event);
            this.socket = null; // Reset the socket
        });
    }

    /**
     * Disconnects from the WebSocket server.
     */
    disconnect(): void {
        if (!this.socket) {
            console.warn("WebSocket is not connected.");
            return;
        }
        this.socket.close();
    }

    /**
     * Sends a message to the WebSocket server.
     * @param message The message object to send.
     */
    send(message: any): void {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            console.error("WebSocket is not connected or not ready.");
            return;
        }
        this.socket.send(JSON.stringify(message));
        console.log("WebSocket message sent:", message);
    }

    /**
     * Sets the handler for incoming messages.
     * @param handler The function to handle messages.
     */
    onMessage(handler: WebSocketEventHandler): void {
        this.onMessageHandler = handler;
    }

    /**
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
