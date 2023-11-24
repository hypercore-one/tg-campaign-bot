from enum import StrEnum
from config.config import Config
import inflect

from utils.format import format_tags, format_links, format_post_criteria, format_time


class Default(StrEnum):
    INFO = '/info\nlist of commands\n'
    CAMPAIGN = '/campaign\ndisplay current campaign details\n',
    ANNOUNCEMENTS = '/announcements\nchannel link\n',
    LEADERBOARD = '/leaderboard\ntop users in the current campaign\n',
    USERNAME = '/username @username\ncampaign data for any Twitter handle\n'
    SCORING = '/scoring\ndescription of scoring calculation\n'


def start(bot_name):
    return ('Welcome, 👽!\n\n'
            f'<b>@{bot_name}</b> is a community-funded Twitter marketing contest.\n'
            'Top participants will be awarded a prize at the end of each campaign.\n'
            'Other participants will be entered in a raffle.\nTheir chances of winning are based on their scores.\n\n'
            'Type <b>/commands</b> for more info')


def info():
    return (f'<b>Commands</b>\n\n'
            f'{Default.ANNOUNCEMENTS}\n'
            f'{Default.CAMPAIGN}\n'
            f'{Default.SCORING}\n'
            f'{Default.LEADERBOARD}\n'
            f'{Default.USERNAME}')


def leaderboard(users):
    if len(users) == 0:
        return 'No data available'

    p = inflect.engine()
    response = '<b>Leaderboard</b>\n'
    for i, user in enumerate(users):
        response += f'<b>{p.ordinal(i + 1)}</b>: <a href="https://twitter.com/{user["username"]}">@{user["username"]}</a> (<b>{user["score"]}</b>)\n'
    return response


def campaign(c):
    return (f'<b>Active Campaign</b>\n'
            f'Time remaining: <b>{format_time(c["end_time"])}</b>\n'
            f'Post criteria: {format_post_criteria(c["post_criteria"])}\n')


def scoring(c):
    response = ('<b>Scoring Information</b>\n'
                'Scores are based on various metrics gathered from Twitter during a campaign, including:\n'
                '- account age, verified status, follower count, etc.\n'
                '- profile metadata: description hash/cash tags, links\n'
                '- posts participating in the campaign\n'
                '    - impressions, likes, retweets, etc.\n\n')

    if c is not None:
        response += ('<b>Valid Data</b>\n'
                     f'- Profile hashtags: {format_tags(c["profile_hashtags_criteria"])}\n'
                     f'- Profile cashtags: {format_tags(c["profile_cashtags_criteria"])}\n'
                     f'- Links (posts/profile): \n{format_links(c["link_criteria"])}'
                     f'- Post character requirement: {c["post_length_criteria"]}')
    return response


def username(user):
    p = inflect.engine()
    return (
        f'<b><a href="https://twitter.com/{user["username"]}">@{user["username"]}</a></b> is in <b>{p.ordinal(user["place"])} place</b>\n'
        f'Score: <b>{user["score"]}</b>\n'
        f'Posts: <b>{user["posts"]}</b>')


def channel():
    return Config.ANNOUNCEMENT_CHANNEL
