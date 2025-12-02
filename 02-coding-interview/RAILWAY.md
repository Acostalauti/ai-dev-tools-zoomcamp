# Deploying to Railway

This project is configured for easy deployment on [Railway](https://railway.app/).

## Prerequisites

- A GitHub account with this repository pushed to it.
- A Railway account.

## Steps

1.  **Log in to Railway** and click **New Project**.
2.  Select **Deploy from GitHub repo**.
3.  Choose this repository.
4.  **Configuration**:
    - Railway will automatically detect the `Dockerfile`.
    - No special configuration is needed.
    - Railway automatically injects a `PORT` environment variable.
    - The `start.sh` script will configure Nginx to listen on this port.
5.  **Deploy**: Click **Deploy Now**.

## How it works

- **Dockerfile**: Builds the frontend and backend, and installs Nginx and Supervisor.
- **start.sh**: A startup script that:
    - Reads the `PORT` environment variable provided by Railway.
    - Updates `nginx.conf` to listen on that port.
    - Starts Supervisor.
- **Supervisor**: Manages two processes:
    - **Nginx**: Serves the frontend and proxies API/WebSocket requests.
    - **Backend**: Runs the Node.js server on port 3000 (internal).

## Troubleshooting

- **Logs**: Check the "Deploy Logs" in Railway if the build fails.
- **App Logs**: Check the "App Logs" to see output from Nginx and the Backend.
