import asyncio
import websockets
import json

async def connect_and_send():
    uri = "ws://192.168.56.101:8080"  # Replace with your WebSocket server URL
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server")
            
            # Example data to send
            data = {
                "message": "Hello Server!"
            }
            
            # Send data to the server
            await websocket.send(json.dumps(data))
            print("Data sent to server")
            
            # Receive response from the server
            response = await websocket.recv()
            print(f"Response from server: {response}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(connect_and_send())