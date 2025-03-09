# Django OCPP Backend for EV Chargers

This repository contains a simple backend module built with Django and Django Channels to communicate with electric vehicle (EV) chargers using the OCPP 1.6 JSON protocol. The solution handles WebSocket connections to process OCPP messages (e.g., BootNotification, StartTransaction) and exposes REST API endpoints for backend control.

## Overview

This project implements an OCPP 1.6 backend server that:

- Accepts WebSocket connections from EV chargers.
- Routes and processes OCPP messages (e.g., BootNotification, StartTransaction).
- Exposes REST endpoints for administrative tasks like listing active chargers and remotely initiating commands.
- Uses Django Channels to handle asynchronous real-time communications.

> Note: In a typical OCPP flow, chargers initiate a BootNotification upon connection. In this implementation, for testing purposes, the backend can also trigger a BootNotification request. If no response is received from the charger within a specified timeout, a simulated response is generated.

## Features

- WebSocket Handling:
    Uses Django Channels to accept and manage connections from multiple chargers concurrently.

- OCPP Message Routing:
    Processes core messages such as BootNotification and StartTransaction.

- REST API:
    Provides endpoints to list connected chargers and send remote commands.

- Timeout Handling:
    Catches and simulates responses if the charger does not respond within the expected timeframe.


## Requirements

- Python 3.10+
- Django 3.x or later
- Django Channels
- Redis (for Channels layer; recommended to use Docker or WSL on Windows)
- OCPP Python library

## Installation
1. Clone the Repository:

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. Create and Activate a Virtual Environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

3. Install Dependencies:

```bash
pip install -r requirements.txt
```

4. Run Redis on Windows

Since the native Windows port of Redis may lack needed commands, it is recommended to run Redis in Docker:

```bash
docker run --name redis -p 6379:6379 -d redis:latest
```

5. Running the Application
- Using Django’s Development Server
If you have Django 3.x or later, running:

```bash
python manage.py runserver
```

will start the server in ASGI mode (provided Channels is configured).

- Using Uvicorn
For a dedicated ASGI server, run:
```bash
uvicorn backend_project.asgi:application --reload
```

## API Endpoints
1. WebSocket Endpoint
Connect to the OCPP WebSocket endpoint:
```bash
ws://localhost:8000/ws/ocpp/<charger_id>/
```
For example, for charger with ID 505:
```bash
wscat -c ws://localhost:8000/ws/ocpp/505/
```

2. REST Endpoints

This backend exposes several REST API endpoints for interacting with connected chargers and for simulating OCPP commands. Below are the details for each endpoint:

1. List Active Chargers
**Endpoint:** GET /api/ocpp/chargers/
**Description:** Returns a list of all currently connected charger IDs.
**Response Example:**
```json
{
    "active_chargers": ["505", "506", "507"]
}
```
2. Remote BootNotification (Remote Start)
**Endpoint:** POST /api/ocpp/start/<charger_id>/
**Description:** Triggers a remote BootNotification command for a specified charger. This is used for testing purposes; normally, the charger should send a BootNotification on connection.
**Parameters:**
- charger_id (URL parameter): The unique identifier of the charger.
**Response Example:**
```json
{
    "status": "Remote BootNotification Command Sent"
}
```
3. Remote Stop Transaction
**Endpoint:** POST /api/ocpp/stop/<charger_id>/
**Description:** Sends a RemoteStopTransaction command to the specified charger. If the charger does not respond within the timeout period, a simulated response is returned.
**Parameters:**
- charger_id (URL parameter): The unique identifier of the charger.
**Response Example:**
```json
{
    "status": "Remote Stop Command Sent"
}
```
4. Charger Status
**Endpoint:** GET /api/ocpp/status/<charger_id>/
**Description:** Retrieves the current status of the specified charger. This endpoint currently returns simulated status data, which can be expanded to include real-time metrics.
**Parameters:**
- charger_id (URL parameter): The unique identifier of the charger.
**Response Example:**
```json
{
    "status": {
        "charger_id": "505",
        "status": "Available",
        "last_seen": "2025-02-26T12:00:00Z"
    }
}
```
5. Transaction Logs
**Endpoint:** GET /api/ocpp/transactions/<charger_id>/
**Description:** Retrieves a list of simulated transaction logs for the specified charger. In a production environment, these logs would be retrieved from a persistent database.
**Parameters:**
- charger_id (URL parameter): The unique identifier of the charger (optional; if omitted, logs for all chargers might be returned).
Response Example:
```json
{
    "transaction_logs": [
        {
            "transaction_id": 12345,
            "charger_id": "505",
            "start_time": "2025-02-26T12:00:00Z",
            "end_time": "2025-02-26T12:30:00Z",
            "status": "Completed"
        },
        {
            "transaction_id": 12346,
            "charger_id": "505",
            "start_time": "2025-02-26T13:00:00Z",
            "end_time": null,
            "status": "Ongoing"
        }
    ]
}
```
6. Remote Authorization
**Endpoint:** POST /api/ocpp/authorize/<charger_id>/
**Description:** Triggers a remote authorization command for a specified charger. This endpoint sends an authorization request with an id_tag and returns a simulated response if the charger does not respond.
**Parameters:**
- charger_id (URL parameter): The unique identifier of the charger.
**Request Body: JSON payload containing:**
- id_tag (string): The identifier to be authorized.
**Response Example:**
```json
{
    "status": "Authorization command sent for id_tag default-id-tag"
}
```
## Testing

- WebSocket Testing:
Use a WebSocket client like wscat or browser developer tools to connect to your endpoint.

- OCPP Simulator:
Consider using an OCPP simulator (e.g., OCPP Chargestation Simulator) to simulate a real EV charger.

- API Testing:
Use Postman or cURL to verify REST endpoints.

## Troubleshooting
- Timeouts:
    If you see timeouts (e.g., for BootNotification), ensure the charger/simulator is connected and responding. For testing, the backend simulates a response if no reply is received within the timeout period.

- Redis Issues:
    On Windows, upgrade Redis using Docker or WSL to support required commands like BZPOPMIN.