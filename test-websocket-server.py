import asyncio
import websockets

async def handle_client(websocket):
    print("Client connected")

    try:
        while True:  # Keep the connection open and continuously listen
            # Receive a message from the client
            message = await websocket.recv()
            print(f"Message received from client: {message}")

            # Send a response to the client
            await websocket.send("Hello from the server!")
            print("Response sent to client")
    except websockets.ConnectionClosed:
        print("Client disconnected")

async def main():
    server = await websockets.serve(handle_client, "localhost", 8080)
    print("Server started")
    print("Listening on ws://localhost:8080")
    print("Waiting for clients to connect....")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
