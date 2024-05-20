from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from config_data import get_json_data

def menu():
    """Menu markup"""
    markup = InlineKeyboardBuilder()
    if get_json_data()['use_ngrok']:
        markup.row(
            InlineKeyboardButton(text='🛰️SSH', callback_data='ssh'), 
            InlineKeyboardButton(text='📢Ping', callback_data='ping'), 
            InlineKeyboardButton(text='💿Backup', callback_data='backup'), 
            InlineKeyboardButton(text='📟Sensors', callback_data='sensors'), 
            InlineKeyboardButton(text='💻Execute command', callback_data='command'), 
            InlineKeyboardButton(text='👨‍💻Dev info', callback_data='dev_info'), width=1
        )
        return markup.as_markup()
    else:
        markup.row(
            InlineKeyboardButton(text='📢Ping', callback_data='ping'), 
            InlineKeyboardButton(text='💿Backup', callback_data='backup'), 
            InlineKeyboardButton(text='📟Sensors', callback_data='sensors'), 
            InlineKeyboardButton(text='💻Execute command', callback_data='command'), 
            InlineKeyboardButton(text='👨‍💻Dev info', callback_data='dev_info'), width=1
        )
        return markup.as_markup()
    
def back_to_menu():
    """Back to main menu markup"""
    markup = InlineKeyboardBuilder(markup=[[InlineKeyboardButton(text='↩️Back', callback_data='menu')]])
    return markup.as_markup()

def sensors_menu():
    """Sensors menu"""
    markup = InlineKeyboardBuilder()
    markup.row(
        InlineKeyboardButton(text='🌡️GPU & CPU Temperature', callback_data='temperature'),
        InlineKeyboardButton(text='🖥Virtual and swap memory', callback_data='virtual_memory'), 
        InlineKeyboardButton(text='👥Logged in server users', callback_data='logged_users'),
        InlineKeyboardButton(text='⏳Server uptime', callback_data='server_uptime'),
        InlineKeyboardButton(text='💾Disk memory', callback_data='disk_memory'),
        InlineKeyboardButton(text='↩️Back', callback_data='menu'), width=1
    )
    return markup.as_markup()

def back_to_sensors_menu():
    """Back to menu of sensors"""
    markup = InlineKeyboardBuilder(markup=[[InlineKeyboardButton(text='↩️Back', callback_data='sensors')]])
    return markup.as_markup()

def backup_menu():
    markup = InlineKeyboardBuilder()
    markup.row(
        InlineKeyboardButton(text='📁Set directories for backup', callback_data='backup_directories'),
        InlineKeyboardButton(text='⏳Edit timeout for backup', callback_data='backup_timeout'), 
        InlineKeyboardButton(text='💾Send backup file', callback_data='send_backup'),
        InlineKeyboardButton(text='↩️Back', callback_data='menu'), width=1
    )
    return markup.as_markup()

def back_to_backup_menu():
    markup = InlineKeyboardBuilder()
    markup.row(
        InlineKeyboardButton(text='↩️Back', callback_data='backup'), width=1
    )
    return markup.as_markup()