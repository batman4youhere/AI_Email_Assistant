import json
import os

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def get_openai_key():
    config = load_config()
    key = config.get("openai_api_key")
    if not key:
        key = input("Enter your OpenAI API Key: ")
        config["openai_api_key"] = key
        save_config(config)
    return key

def get_recheck_interval():
    config = load_config()
    interval = config.get("recheck_interval")
    if not interval:
        interval = input("Enter email recheck interval in seconds (default 30): ")
        try:
            interval = int(interval)
        except:
            interval = 30
        config["recheck_interval"] = interval
        save_config(config)
    return interval
