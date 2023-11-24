import yaml


class Config:
    with open('config.yml', 'r') as file:
        config_data = yaml.safe_load(file)

    TG_BOT_TOKEN = config_data['TG_BOT_TOKEN']
    ANNOUNCEMENT_CHANNEL = config_data['ANNOUNCEMENT_CHANNEL']
    SUPABASE_URL = config_data['SUPABASE_URL']
    SUPABASE_ANON_KEY = config_data['SUPABASE_ANON_KEY']
