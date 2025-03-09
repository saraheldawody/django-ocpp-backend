import json
from channels.generic.websocket import AsyncWebsocketConsumer
from ocpp_app.ocpp_handlers import ChargePoint as OCPPChargePointHandler
from asyncio import create_task

# In-memory storage for active chargers (for demo purposes)
active_chargers = {}

class OCPPConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract the charger id from the URL (e.g., /ws/ocpp/<charger_id>/)
        self.charger_id = self.scope['url_route']['kwargs']['charger_id']
        await self.accept()
        
        # Instantiate your OCPP charge point handler passing self as the websocket wrapper.
        self.cp_handler = OCPPChargePointHandler(self.charger_id, self)
        active_chargers[self.charger_id] = self
        
        # Start processing messages in the background.
        self.listener_task = create_task(self.cp_handler.start())
        print(f"Charger {self.charger_id} connected.")

    async def disconnect(self, close_code):
        # Clean up the active charger on disconnect
        if self.charger_id in active_chargers:
            del active_chargers[self.charger_id]
        if self.listener_task:
            self.listener_task.cancel()
        print(f"Charger {self.charger_id} disconnected.")

    async def receive(self, text_data):
        # When a message is received from the charger, hand it off to the OCPP logic.
        message = json.loads(text_data)
        # Route the message using the OCPP library’s routing logic.
        await self.cp_handler.route_message(message)

    # Helper function to send JSON messages via WebSocket.
    async def send_json(self, content):
        await self.send(text_data=json.dumps(content))
