# SSH operations with server

from config_data import get_json_data
from pyngrok import ngrok
import paramiko

# Create ngrok SSH-tunnel
def start_ngrok():
    """Create SSH-Tunnel with ngrok"""
    ngrok.set_auth_token(get_json_data()['ngrok_auth_token'])
    return ngrok.connect("22", "tcp").public_url[6:]

# Execute command on server
def execute_command(command: str):
    """Execute command on server"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=get_json_data()['host'], username=get_json_data()['user'], password=get_json_data()['user_password'], port=get_json_data()['port'])
    stdin, stdout, stderr = client.exec_command(command=command)
    client.close()
    return str(stdout.read() + stderr.read())