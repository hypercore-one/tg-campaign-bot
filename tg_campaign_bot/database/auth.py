from supabase import create_client, Client

from config.config import Config


def init_client():
    return create_client(Config.SUPABASE_URL, Config.SUPABASE_ANON_KEY)


class Supabase:
    client: Client = init_client()
