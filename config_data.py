import json

def get_json_data() -> str:
    with open('config.json') as json_file: return json.load(json_file)

def write_json_data(data):
    with open('config.json', 'w', encoding='utf-8') as json_file: json.dump(data, json_file, ensure_ascii=False, indent=4)