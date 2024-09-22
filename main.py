

import zipfile
from telethon import TelegramClient, errors
import uuid
import os
import asyncio
import pyminizip


BOT_USER_NAME = 'up4me004bot'

FILE_CHUCK_SIZE = int(50 * 1024)
script_dir = os.path.dirname(os.path.abspath(__file__))
temp_dir = os.path.join(script_dir, 'temp')
os.makedirs(temp_dir, exist_ok=True)

api_id = 1197576
api_hash = '93623f19301332e9d02e7eec57a91cf4'

client = TelegramClient('initial_session', api_id, api_hash)

async def uploadFile(fileName):
    await client.start()
    with open('/Users/omarammura/Downloads/resume.pdf','rb') as op:
    # file_data = bytearray()  # Initialize an empty bytearray
    # Assume file_data is populated with the file contents elsewhere
    # with file_data as op:
        file_number = 0
        united_id = uuid.uuid4()
        await client.send_message(BOT_USER_NAME, f"----- BEGIN FILE [{fileName}] ID:{united_id} ------")
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
        await client.send_message(BOT_USER_NAME, f"----- END FILE [filename] ID:{united_id} ------")
        

async def getFile(fileId,fileName):
    fileCount = 0
    await client.start()
    fileId = fileId.strip()
    async for message in client.iter_messages(BOT_USER_NAME, search=fileId):
        if message.media:
            await message.download_media(file=f"{fileCount}_{fileId}.zip")
            fileCount += 1
    print(fileCount)
    for i in range(fileCount):
        zip_file_path = f"{i}_{fileId}.zip"
        if os.path.exists(zip_file_path):
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall('temp',pwd=b"004")
            os.remove(zip_file_path)  # Remove the zip file after extraction
        else:
            print(f"File not found: {zip_file_path}")
    
    # Combine extracted files
    combined_file_path = os.path.join('temp', f"combined_{fileId}")
    with open(combined_file_path + fileName.split(".")[1], 'wb') as combined_file:
        for i in range(fileCount):
            temp_file_path = os.path.join('temp', f"{i}_{fileId}")
            if os.path.exists(temp_file_path):
                with open(temp_file_path + f"{os.path.splitext(fileName)}" , 'rb') as temp_file:
                    combined_file.write(temp_file.read())
                os.remove(temp_file_path)
    
    print(f"Combined file created: {combined_file_path}")
            

# asyncio.run(uploadFile())
asyncio.run(getFile("2cb4fb09-b7b2-4c4b-b686-431f67b6326b"))

