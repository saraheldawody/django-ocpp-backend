import json
from django.http import JsonResponse
from asgiref.sync import async_to_sync
from ocpp_app.consumers import active_chargers
from rest_framework.views import APIView

class ListChargers(APIView):
    """Return a list of active charger IDs."""
    def get(self, request):
        return JsonResponse({"active_chargers": list(active_chargers.keys())})


class RemoteStart(APIView):
    """Trigger a remote BootNotification command for a charger."""
    def post(self, request, charger_id):
        if charger_id in active_chargers:
            consumer = active_chargers[charger_id]
            async_to_sync(consumer.cp_handler.send_boot_notification)()
            return JsonResponse({"status": "Remote BootNotification Command Sent"})
        else:
            return JsonResponse({"error": "Charger not found"}, status=404)


class RemoteStop(APIView):
    """Trigger a remote stop transaction command for a charger.
    
    Note: Ensure that you have implemented `send_remote_stop_transaction` in your OCPP handler.
    """
    def post(self, request, charger_id):
        if charger_id in active_chargers:
            consumer = active_chargers[charger_id]
            async_to_sync(consumer.cp_handler.send_remote_stop_transaction)()
            return JsonResponse({"status": "Remote Stop Command Sent"})
        else:
            return JsonResponse({"error": "Charger not found"}, status=404)


class ChargerStatus(APIView):
    """Get the current status of a charger.
    
    This is a simulated status. In a production setup, you might retrieve real-time data
    from the charger or a persistent datastore.
    """
    def get(self, request, charger_id):
        if charger_id in active_chargers:
            # Simulate charger status; you can enhance this with real data if available.
            status = {
                "charger_id": charger_id,
                "status": "Available",  # Could be "Charging", "Faulted", etc.
                "last_seen": "2025-02-26T12:00:00Z"
            }
            return JsonResponse({"status": status})
        else:
            return JsonResponse({"error": "Charger not found"}, status=404)


class TransactionLogs(APIView):
    """Retrieve simulated transaction logs.
    
    In a production system, transaction logs would be stored in a database.
    """
    def get(self, request, charger_id=None):
        if charger_id not in active_chargers:
            return JsonResponse({"error": "Charger not found"}, status=404)
        logs = [
            {"transaction_id": 12345, "start_time": "2025-02-26T12:00:00Z", "status": "Active", "command": "StartTransaction"},
            {"transaction_id": 67890, "start_time": "2025-02-26T12:30:00Z", "status": "Completed", "command": "StopTransaction"},
            #etc.. should be got from DB
        ]
        return JsonResponse({"transaction_logs": logs})


class RemoteAuthorize(APIView):
    """Trigger a remote authorize command for a given id_tag.
    
    This endpoint simulates sending an authorization request to the charger.
    """
    def post(self, request, charger_id):
        if charger_id in active_chargers:
            # In a real implementation, you'd extract the id_tag from the request data
            id_tag = request.data.get("id_tag", "default-id-tag")
            consumer = active_chargers[charger_id]
            async_to_sync(consumer.cp_handler.send_authorize)(id_tag)
            return JsonResponse({"status": f"Authorization command sent for id_tag {id_tag}"})
        else:
            return JsonResponse({"error": "Charger not found"}, status=404)
