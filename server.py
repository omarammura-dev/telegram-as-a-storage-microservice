import grpc
from concurrent import futures
import telegram_as_storage_pb2
import telegram_as_storage_pb2_grpc
import zipfile
from telethon import TelegramClient, errors
import uuid
import base64
import io
import os
from grpc_reflection.v1alpha import reflection
import asyncio
import pyminizip


BOT_USER_NAME = os.getenv("BOT_NAME")


FILE_CHUCK_SIZE = int(1.49 * 1024**3)
script_dir = os.path.dirname(os.path.abspath(__file__))
temp_dir = os.path.join(script_dir, 'temp')
os.makedirs(temp_dir, exist_ok=True)

api_id = int(os.getenv("APP_ID"))
api_hash = os.getenv("API_HASH")


client = TelegramClient('initial_session', api_id, api_hash)


class StorageServicer(telegram_as_storage_pb2_grpc.StorageServicer):
    async def UploadFile(self, request, context):
        async with client:
            fileByteArray = base64.b64decode(request.fileData)
            file_number = 0
            united_id = uuid.uuid4()
            await client.send_message(BOT_USER_NAME, f"----- BEGIN FILE [{request.filename}] ID:{united_id} ------")
            with io.BytesIO(fileByteArray) as op:
                while True:
                    data = op.read(FILE_CHUCK_SIZE)
                    if not data:
                        break
                    temp_file_path = os.path.join(temp_dir, f'{file_number}_{united_id}')
                    with open(temp_file_path, 'wb') as packet:
                        packet.write(data)
                    zip_file_path = os.path.join(script_dir, f'{file_number}_{united_id}.zip')
                    pyminizip.compress(temp_file_path, None, zip_file_path, "004", 5)
                    file_number += 1
                    try:
                        await client.send_file(BOT_USER_NAME, zip_file_path)
                    except errors.FilePartsInvalidError:
                        print(f"Failed to send file: {zip_file_path}")
                        print("Error: Not an existing file, an HTTP URL or a valid bot-API-like file ID")
                    finally:
                        os.remove(zip_file_path)
                        os.remove(temp_file_path)
            
            await client.send_message(BOT_USER_NAME, f"----- END FILE [{request.filename}] ID:{united_id} ------")
            return telegram_as_storage_pb2.UploadFileResponse(fileId=str(united_id))

    async def GetFile(self, request, context):
        async with client:
            fileCount = 0
            fileId = request.fileId.strip()
            fileName = request.filename

            async for message in client.iter_messages(BOT_USER_NAME, search=fileId):
                if message.media:
                    await message.download_media(file=f"{fileCount}_{fileId}.zip")
                    fileCount += 1

            for i in range(fileCount):
                zip_file_path = f"{i}_{fileId}.zip"
                if os.path.exists(zip_file_path):
                    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                        zip_ref.extractall('temp', pwd=b"004")
                    os.remove(zip_file_path)
                else:
                    print(f"File not found: {zip_file_path}")

            combined_file_path = os.path.join('temp', f"combined_{fileId}")
            with open(combined_file_path + os.path.splitext(fileName)[1], 'wb') as combined_file:
                for i in range(fileCount):
                    temp_file_path = os.path.join('temp', f"{i}_{fileId}")
                    if os.path.exists(temp_file_path):
                        with open(temp_file_path, 'rb') as temp_file:
                            combined_file.write(temp_file.read())
                        os.remove(temp_file_path)

            with open(combined_file_path + os.path.splitext(fileName)[1], 'rb') as file:
                file_content = file.read()
            
            os.remove(combined_file_path + os.path.splitext(fileName)[1])

            return telegram_as_storage_pb2.GetFileResponse(file=base64.b64encode(file_content).decode())
        
    async def DeleteFile(self, request, context):
        fileId = request.fileId.strip()
        print(f"start delete: {fileId}")
        if not fileId:
            return telegram_as_storage_pb2.DeleteFileResponse(ok=False)
        
        async with client:
            deleted_count = 0
            async for message in client.iter_messages(BOT_USER_NAME, search=fileId):
                try:
                    await message.delete()
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting message: {e}")
            
            if deleted_count == 0:
                return telegram_as_storage_pb2.DeleteFileResponse(ok=False)
        
        return telegram_as_storage_pb2.DeleteFileResponse(ok=True)

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    telegram_as_storage_pb2_grpc.add_StorageServicer_to_server(StorageServicer(), server)
    
    # Add reflection service to the server
    SERVICE_NAMES = (
        telegram_as_storage_pb2.DESCRIPTOR.services_by_name['Storage'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())
