import { useEffect } from "react";

export function useWebSocket(onMessage) {

    useEffect(() => {

        const socket = new WebSocket(
            "ws://127.0.0.1:8000/ws"
        );

        socket.onopen = () => {
            console.log("✅ Connected");
        };

        socket.onmessage = (event) => {

            const message = JSON.parse(event.data);

            onMessage(message);

        };

        socket.onclose = () => {
            console.log("Disconnected");
        };

        return () => socket.close();

    }, []);
}