from enum import StrEnum
from config.config import Config
import inflect

from utils.format import format_tags, format_links, format_post_criteria, format_time


class Default(StrEnum):
    INFO = '`/info`\nlist of commands\n'
    CAMPAIGN = '`/campaign`\ndisplay current campaign details\n',
    ANNOUNCEMENTS = '`/announcements`\nchannel link\n',
    LEADERBOARD = '`/leaderboard`\ntop users in the current campaign\n',
    USERNAME = '`/username @username`\ncampaign data for any Twitter handle\n'
    SCORING = '`/scoring`\ndescription of scoring calculation\n'


def start(bot_name):
    return ('Welcome, 👽!\n\n'
            f'*@{bot_name}* is a community-funded Twitter marketing contest.\n'
            'Top participants will be awarded a prize at the end of each campaign.\n'
            'Other participants will be entered in a raffle.\nTheir chances of winning are based on their scores.\n\n'
            'Type `/commands` for more info')


def info():
    return (f'*Commands*\n\n'
            f'{Default.ANNOUNCEMENTS}\n'
            f'{Default.CAMPAIGN}\n'
            f'{Default.SCORING}\n'
            f'{Default.LEADERBOARD}\n'
            f'{Default.USERNAME}')


def leaderboard(users):
    if len(users) == 0:
        return 'No data available'

    p = inflect.engine()
    response = '*Leaderboard*\n'
    for i, user in enumerate(users):
        response += f'*{p.ordinal(i + 1)}*: @{user["username"]} (*{user["score"]}*)\n'
    return response


def campaign(c):
    return (f'*Active Campaign*\n'
            f'Time remaining: *{format_time(c["end_time"])}*\n'
            f'Post criteria: {format_post_criteria(c["post_criteria"])}\n')


def scoring(c):
    response = ('*Scoring Information*\n'
                'Scores are based on various metrics gathered from Twitter during a campaign, including:\n'
                '- account age, verified status, follower count, etc.\n'
                '- profile metadata: description hash/cash tags, links\n'
                '- posts participating in the campaign\n'
                '    - impressions, likes, retweets, etc.\n\n')

    if c is not None:
        response += ('*Valid Data*\n'
                     f'- Profile hashtags: {format_tags(c["profile_hashtags_criteria"])}\n'
                     f'- Profile cashtags: {format_tags(c["profile_cashtags_criteria"])}\n'
                     f'- Links (posts/profile): \n{format_links(c["link_criteria"])}'
                     f'- Post character requirement: {c['post_length_criteria']}')
    return response


def username(user):
    p = inflect.engine()
    return (f'*@{user["username"]}* is in *{p.ordinal(user["place"])} place*\n'
            f'Score: *{user["score"]}*\n'
            f'Posts: *{user["posts"]}*')


def channel():
    return Config.ANNOUNCEMENT_CHANNEL
