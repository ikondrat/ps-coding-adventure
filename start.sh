#!/bin/bash
# Start the application
docker compose up -d backend

cd frontend && npm i && npm run dev