
from config_data import get_json_data, write_json_data
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from pythread import AsyncThreadManager
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from threading import Thread
from backup import Backup
import datetime
import markups
import sensors
import ssh

# Initialize variables
dp = Dispatcher(storage=MemoryStorage())
bot = Bot(get_json_data()['bot_token'], parse_mode='html')
threadmanager = AsyncThreadManager()
if get_json_data()['use_ngrok']: ssh_tunnel = ssh.start_ngrok()

# Set StateMachine
class State(StatesGroup):
    backup_directory = State()
    backup_timeout = State()
    command = State()

@dp.message(Command('start'))
async def start(message: Message):
    if message.from_user.id in get_json_data()['linux_users']:
        await message.reply(text=f'<b>Server menu</b>', reply_markup=markups.menu())

@dp.callback_query(StateFilter(None))
async def callback(call: CallbackQuery, state: FSMContext):
    match call.data: 
        case 'ssh': 
            await call.message.edit_text(text=f'<b>[{datetime.datetime.now()}]:</b>\nConnect url (ngrok):\n<code>{ssh_tunnel}</code>', reply_markup=markups.back_to_menu())
        case 'ping': 
            await call.message.edit_text(text=f"<b>[{datetime.datetime.now()}]:</b>\nPong! I'm active", reply_markup=markups.back_to_menu())
        case 'backup':
            await call.message.edit_text(text=f"<b>[{datetime.datetime.now()}]:\nBackup menu</b>", reply_markup=markups.backup_menu())
        case 'backup_directories':
            await call.message.edit_text(text=f"""<b>[{datetime.datetime.now()}]:\n🗂Enter directories for further backup, for example:\n/root/project\n/home/user/project</b>""", reply_markup=markups.back_to_backup_menu())
            await state.set_state(State.backup_directory)
        case 'backup_timeout':
            await call.message.edit_text(text=f"<b>[{datetime.datetime.now()}]:\n🗂Enter timeout for backup (in hours, you can use a fraction like 0.6):</b>", reply_markup=markups.back_to_backup_menu())
            await state.set_state(State.backup_timeout)
        case 'send_backup':
            await call.message.edit_text(text=f"<b>[{datetime.datetime.now()}]:\nBackup creating, please, wait...</b>", reply_markup=markups.back_to_backup_menu())
            Thread(target=Backup.create_backup).start()
        case 'sensors': 
            await call.message.edit_text(text=f"<b>[{datetime.datetime.now()}]:\nSensors menu</b>", reply_markup=markups.sensors_menu())
        case 'command': 
            await call.message.edit_text(text=f"<b>[{datetime.datetime.now()}]:\n👩🏻‍💻Enter command do you need to execute:</b>", reply_markup=markups.back_to_menu())
            await state.set_state(State.command)
        case 'temperature': 
            await call.message.edit_text(text=f"<b>[{datetime.datetime.now()}]:\n{sensors.get_temp()}</b>", 
            reply_markup=markups.back_to_sensors_menu())
        case 'virtual_memory':
            await call.message.edit_text(text=f"<b>[{datetime.datetime.now()}]:\n{sensors.used_memory()}</b>", 
            reply_markup=markups.back_to_sensors_menu())
        case 'logged_users':
            await call.message.edit_text(text=f"<b>[{datetime.datetime.now()}]:\n{sensors.logged_users()}</b>", 
            reply_markup=markups.back_to_sensors_menu())
        case 'server_uptime':
            await call.message.edit_text(text=f"<b>[{datetime.datetime.now()}]:\n{sensors.server_uptime()}</b>", 
            reply_markup=markups.back_to_sensors_menu())
        case 'disk_memory':
            await call.message.edit_text(text=f"<b>[{datetime.datetime.now()}]:\n{sensors.disk_usage()}</b>", 
            reply_markup=markups.back_to_sensors_menu())
        case 'dev_info':
            await call.message.edit_text(text=f"<b>[{datetime.datetime.now()}]:\n👨‍💻Bot created by @merbuz_dev\n📌Bot version: <code>2.4</code></b>", 
            reply_markup=markups.back_to_menu())
        case 'menu': 
            await call.message.edit_text(text=f'<b>Server menu</b>', reply_markup=markups.menu())

@dp.callback_query(lambda call: call.data == 'backup')
async def cancel_backup_edit(call: CallbackQuery, state: FSMContext):
    # Cancel backup edit
    await state.clear()
    await call.message.edit_text(text=f'<b>Backup menu</b>', reply_markup=markups.backup_menu())

@dp.message(State.backup_directory)
async def edit_backup_directories(message: Message, state: FSMContext):
    # Edit backup directories
    old_data = get_json_data()
    try: 
        # Try write new directories
        directory = await state.update_data(directory=[directory for directory in message.text.lower().split('\n')])
        Backup.change_backup_directories(directory['directory'])
        await threadmanager.stop_task('backup_create')
        await threadmanager.start_task(name='backup_create', coro_func=Backup.backup_create_task) 
        await bot.send_message(chat_id=message.chat.id, text=f'<b>✅Paths have been successfully changed!</b>')
        await state.clear()
    except: 
        # Return old data
        write_json_data(data=old_data)
        await bot.send_message(chat_id=message.chat.id, text=f'<b>❌Failed to change paths!</b>')
        await state.clear()

@dp.message(State.backup_timeout)
async def edit_backup_timeout(message: Message, state: FSMContext):
    try: 
        # Try write new timeout
        timeout = await state.update_data(timeout=float(message.text.lower()))
        Backup.change_backup_timeout(timeout['timeout'])
        await threadmanager.stop_task('backup_create')
        await threadmanager.start_task(name='backup_create', coro_func=Backup.backup_create_task) 
        await bot.send_message(chat_id=message.chat.id, text=f'<b>✅The timeout have been successfully changed!</b>')
        await state.clear()
    except: 
        # If failed
        await bot.send_message(chat_id=message.chat.id, text=f'<b>❌Failed to change timeout!</b>')
        await state.clear()
    
@dp.callback_query(lambda call: call.data == 'menu')
async def cancel_execute_command(call: CallbackQuery, state: FSMContext):
    # Cancel command executing
    await state.clear()
    await call.message.edit_text(text=f'<b>Server menu</b>', reply_markup=markups.menu())

@dp.message(State.command)
async def execute_command(message: Message, state: FSMContext):
    # Execute command and send the result
    command = await state.update_data(command=message.text.lower())
    print(command['command'])
    executing = await bot.send_message(chat_id=message.chat.id, text=f'<b>⏳Command executing, please wait...</b>')
    result = ssh.execute_command(command=command['command'])
    await executing.delete()
    await bot.send_message(chat_id=message.chat.id, text=result)
    await state.clear()

async def main():
    # Send message every admin on start
    for user in get_json_data()['linux_users']: 
        if get_json_data()['use_ngrok']: await bot.send_message(user, f'<b>[{datetime.datetime.now()}]:</b>\nServer turned on.\nConnect url (ngrok):\n<code>{ssh_tunnel}</code>')
        else: await bot.send_message(user, f'<b>[{datetime.datetime.now()}]:</b>\nServer turned on', parse_mode='html')
    
    # Start backup task
    await threadmanager.start_task(name='backup_listener', coro_func=Backup.backup_finder, bot=bot) 
    await threadmanager.start_task(name='backup_create', coro_func=Backup.backup_create_task) 
    
    # Start bot
    await dp.start_polling(bot)
