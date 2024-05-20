# Merbuz-Systems
a simple bot for your own server on micro-pc...

# Install bot
1. Install archive from github and unpack
2. ```pip install -r requirements.txt```
3. edit config
4. ```python main.py &```

# Edit config
![изображение](https://github.com/Merbuz/Merbuz-Systems/assets/75749391/291767a2-1c99-4207-ab3f-b961107f79d6)\n
bot_token - telegram bot token from bot father\n
use_ngrok - use ngrok service if you have not white ip\n
ngrok_auth_token - ngrok token service\n
backup_timeout_in_hours - timeout between backups in hours\n
backup_directories - list of directories do you need to backup\n
host - ip of your server\n
port - 22 (don't change)
user - user do you need to use on server (use root)
user_password - password of your linux user
linux_users - list of users in telegram bot (put id of your telegram account here)
