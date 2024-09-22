
# Telegram File Storage Service

This project implements a gRPC-based file storage service that uses Telegram as the backend storage medium. It allows users to upload, retrieve, and delete files using Telegram's infrastructure.

## Features

- Upload files to Telegram
- Retrieve files from Telegram
- Delete files from Telegram
- Chunked file handling for large files
- File encryption using ZIP compression

## Technologies Used

- Python 3.12
- gRPC
- Protocol Buffers
- Telethon (Telegram client library)
- Docker
- GitLab CI/CD

## Project Structure

The main components of the project are:

1. `server.py`: Contains the gRPC server implementation and the core logic for file operations.
2. `telegram_as_storage_pb2.py` and `telegram_as_storage_pb2_grpc.py`: Generated gRPC code from the Protocol Buffer definition.
3. `telegram-as-storage.proto`: Protocol Buffer definition for the storage service.
4. `.gitlab-ci.yml`: GitLab CI/CD configuration for building, testing, and deploying the service.

## Setup and Installation

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up the following environment variables:
   - `BOT_NAME`: Your Telegram bot username
   - `APP_ID`: Your Telegram API ID
   - `API_HASH`: Your Telegram API Hash

## Usage

To start the gRPC server:
