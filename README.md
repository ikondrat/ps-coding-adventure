# TODO List Application with Electron

This guide will help you set up and run a TODO list application using Electron, Docker, and Docker Compose for both the backend and frontend environments.

---

## Prerequisites

Make sure you have **Docker** and **Docker Compose** installed on your machine.

---

## Getting Started

### 1. Start the Backend Server

To start the backend, run the following command:

```bash
docker-compose up backend
```

This will launch the backend server on port 8000, along with a PostgreSQL instance as required.

Backend API:
Access the backend at http://localhost:8000.

API Documentation:
View interactive API documentation at http://localhost:8000/docs.

### 2. Start the Frontend Application

Navigate to the frontend directory, then install dependencies and start the frontend:

```bash
cd frontend
npm install && npm run dev
```

### 2. Start the Frontend Application

To streamline the setup, a start.sh script has been created to start both backend and frontend services simultaneously. Run it with:

```bash
./start.sh
```

This script will handle starting all necessary services, making it easier to develop and test the application as a unified environment.
