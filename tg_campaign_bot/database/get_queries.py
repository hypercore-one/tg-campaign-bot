import json

from postgrest import APIResponse

from database.auth import Supabase
from database.helper import unpack
from database.tables import Table


def get_user(username):
    result = unpack(json.loads(APIResponse.model_dump_json(
        Supabase.client.table(Table.USERS).select('id,username,score').execute())))

    for i, user in enumerate(result):
        if str(user['username']).lower() == str(username).lower():
            posts = get_user_posts(user['id'])
            return {
                'username': user['username'],
                'score': user['score'],
                'place': i + 1,
                'posts': len(posts),
            }
    return None


def get_top_users():
    return unpack(json.loads(APIResponse.model_dump_json(
        Supabase.client.table(Table.USERS).select('username,score').order('score.desc').limit(5).execute())))


def get_user_posts(id):
    return unpack(json.loads(APIResponse.model_dump_json(
        Supabase.client.table(Table.POSTS).select('id').eq('author_id', id).execute())))


def get_current_campaign():
    try:
        return unpack(json.loads(APIResponse.model_dump_json(
            Supabase.client.table(Table.CAMPAIGNS).select("*").eq("active", True).execute())))[0]
    except:
        return None


def get_all_scores_current_campaign():
    return unpack(json.loads(
        APIResponse.model_dump_json(
            Supabase.client.table(Table.USERS).select("score").execute())))
