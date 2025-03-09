import asyncio
from ocpp.v16 import call, call_result
from ocpp.v16 import ChargePoint as OCPPChargePoint
from ocpp.routing import on

class ChargePoint(OCPPChargePoint):
    async def send_boot_notification(self):
        request = call.BootNotification(
            charge_point_model="EVSE-123",
            charge_point_vendor="EV-Charger Inc."
        )
        try:
            # Using a shorter timeout for testing purposes
            response = await asyncio.wait_for(self.call(request), timeout=5)
            print(f"Boot Notification Response: {response}")
        except asyncio.TimeoutError:
            # Simulate a BootNotification response if charger doesn't reply
            response = call_result.BootNotification(
                current_time="2025-02-26T12:00:00Z",
                interval=10,
                status="Accepted"
            )
            print("No response received for BootNotification; simulating response.")
        return response

    @on("BootNotification")
    async def on_boot_notification(self, charge_point_model, charge_point_vendor, **kwargs):
        print(f"Received BootNotification from {charge_point_model}")
        return call_result.BootNotification(
            current_time="2025-02-26T12:00:00Z",
            interval=10,
            status="Accepted"
        )

    @on("StartTransaction")
    async def on_start_transaction(self, id_tag, connector_id, meter_start, **kwargs):
        print(f"Charging started on connector {connector_id} for ID {id_tag}")
        return call_result.StartTransaction(
            transaction_id=12345,
            id_tag_info={"status": "Accepted"}
        )

    async def send_remote_stop_transaction(self):
        request = call.RemoteStopTransaction(transaction_id=12345)
        try:
            # Using a 5-second timeout for testing; adjust as needed
            response = await asyncio.wait_for(self.call(request), timeout=5)
            print(f"Remote Stop Transaction Response: {response}")
        except asyncio.TimeoutError:
            # Simulate a response if no reply is received
            response = call_result.RemoteStopTransaction(status="Accepted")
            print("No response received for RemoteStopTransaction; simulating response.")
        return response

    async def send_authorize(self, id_tag):
        request = call.Authorize(id_tag=id_tag)
        try:
            response = await asyncio.wait_for(self.call(request), timeout=5)
            print(f"Authorize Response: {response}")
        except asyncio.TimeoutError:
            # Simulate an authorization response with the correct parameter
            response = call_result.Authorize(id_tag_info={"status": "Accepted"})
            print("No response received for Authorize; simulating response.")
        return response
