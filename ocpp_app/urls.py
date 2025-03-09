from django.urls import path
from ocpp_app.views import ListChargers, RemoteStart, RemoteStop, ChargerStatus, TransactionLogs, RemoteAuthorize

urlpatterns = [
    path('chargers/', ListChargers.as_view(), name='list_chargers'),
    path('start/<str:charger_id>/', RemoteStart.as_view(), name='remote_start'),
    path('stop/<str:charger_id>/', RemoteStop.as_view(), name='remote_stop'),
    path('status/<str:charger_id>/', ChargerStatus.as_view(), name='charger_status'),
    path('transactions/<str:charger_id>/', TransactionLogs.as_view(), name='transaction_logs'),
    path('authorize/<str:charger_id>/', RemoteAuthorize.as_view(), name='remote_authorize'),
]
