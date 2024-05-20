# Save files for backup

from config_data import get_json_data, write_json_data
from aiogram.types import FSInputFile
from datetime import datetime, date
from threading import Thread
from aiogram import Bot
import asyncio
import zipfile
import os

class Backup:
    backup_name = ''
    backup_status = ''
    
    def change_backup_timeout(hours: int):
        data = get_json_data()
        data['backup_timeout_in_hours'] = hours
        write_json_data(data)

    def change_backup_directories(list_of_directories: list[str]):
        data = get_json_data()
        data['backup_directories'] = list_of_directories
        write_json_data(data)

    async def backup_finder(bot: Bot):
        while True:
            await asyncio.sleep(1)
            if Backup.backup_name != '':
                for user in get_json_data()['linux_users']: 
                    await bot.send_document(chat_id=user, document=FSInputFile(path=Backup.backup_name))
                os.remove(Backup.backup_name)
                # Reset all data
                Backup.backup_name = ''
                Backup.backup_status = '' 
        
    def create_backup():
        if Backup.backup_status != 'creating':
            Backup.backup_status = 'creating'
            filename = f'backup_{date(datetime.now().year, datetime.now().month, datetime.now().day)}_{datetime.now().hour}-{datetime.now().minute}-{datetime.now().second}.zip'
            with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED, True) as myzip:
                for source_folder in get_json_data()['backup_directories']:
                    for root, dirs, files in os.walk(source_folder):
                        for file in files:
                            path = os.path.join(root, file)
                            myzip.write(path)
            Backup.backup_name = filename

    async def backup_create_task():
        while True:
            await asyncio.sleep(get_json_data()['backup_timeout_in_hours'] * 3600)
            Thread(target=Backup.create_backup).start()