# Parameters of server

from datetime import datetime
from uptime import boottime
import psutil

def get_temp() -> str:
    """Temperature of GPU and CPU"""
    cpu_temp = round(psutil.sensors_temperatures()['cpu_thermal'][0][1], 1)
    gpu_temp = round(psutil.sensors_temperatures()['gpu_thermal'][0][1], 1)
    return f"🌡️CPU Temperature: {cpu_temp}°C\n🌡️GPU Temperature: {gpu_temp}°C"

def used_memory() -> str:
    """Used RAM and SWAP memory"""
    swap_memory_used = round(psutil.swap_memory()[1] / 1024 / 1024, 1)
    swap_memory = round(psutil.swap_memory()[0] / 1024 / 1024, 1)
    ram_used = round(psutil.virtual_memory()[1] / 1024 / 1024, 1)
    ram = round(psutil.virtual_memory()[0] / 1024 / 1024, 1)
    return f"🖥️{ram_used} MB of RAM memory used out of {ram} MB\n💿{swap_memory_used} MB of SWAP memory used out of {swap_memory} MB"

def logged_users() -> str:
    """Logged users in server"""
    users = '👨‍💻Logged users at this moment:\n'
    for user in psutil.users():
        users += f'{user[0]}\n'
    return users

def server_uptime() -> str:
    """Server uptime"""
    return f'⬆️The server uptime is {datetime.now() - boottime()}'

def disk_usage() -> str:
    """Used server memory on disk"""
    disk_memory_used = round(psutil.disk_usage('/')[1] / 1024 / 1024, 1)
    disk_memory = round(psutil.disk_usage('/')[0] / 1024 / 1024, 1)
    return f'💾{disk_memory_used} MB of disk memory used out of {disk_memory} MB'