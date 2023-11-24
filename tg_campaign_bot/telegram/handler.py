from telebot import TeleBot

from config.config import Config
from database.get_queries import get_top_users, get_user, get_current_campaign
from telegram.responses import start, info, leaderboard, username, Default, channel, campaign, scoring
from utils.format import sanitize_output
from utils.logger import Logger


class TelegramHandler:
    rate_limiter = {}
    cooldown = 5  # seconds

    def __init__(self):
        self.bot = TeleBot(Config.TG_BOT_TOKEN)
        self.bot_username = self.bot.get_me().username
        self.start_command = self.bot.message_handler(commands=['start'])(self.start_command)
        self.info_command = self.bot.message_handler(commands=['info', 'commands', 'help'])(self.info_command)
        self.scoring_command = self.bot.message_handler(commands=['scoring'])(self.scoring_command)
        self.leaderboard_command = self.bot.message_handler(commands=['leaderboard'])(self.leaderboard_command)
        self.username_command = self.bot.message_handler(commands=['username'])(self.username_command)
        self.campaign_command = self.bot.message_handler(commands=['campaign'])(self.campaign_command)
        self.channel_command = self.bot.message_handler(commands=['announcements', 'channel'])(self.channel_command)

    def run(self):
        Logger.logger.info('Initializing Telegram Bot')
        self.bot.infinity_polling()

    def reply(self, message, text):
        self.bot.send_message(chat_id=message.chat.id, text=sanitize_output(text), parse_mode='MarkdownV2')

    def check_rate_limit(self, message):
        if message.chat.id in self.rate_limiter:
            delta = message.date - self.rate_limiter[message.chat.id]
            if delta < self.cooldown:
                self.reply(message, f'Try again in {delta} seconds')
                return False
        self.rate_limiter[message.chat.id] = message.date
        return True

    def start_command(self, message):
        if message.chat.type == 'private':
            self.reply(message, start(self.bot_username))

    def info_command(self, message):
        self.reply(message, info())

    def leaderboard_command(self, message):
        if self.check_rate_limit(message):
            users = get_top_users()
            self.reply(message, leaderboard(users))

    def scoring_command(self, message):
        if self.check_rate_limit(message):
            c = get_current_campaign()
            self.reply(message, scoring(c))

    def username_command(self, message):
        if self.check_rate_limit(message):
            split = message.text.split(' ')
            if len(split) == 2:
                if split[1][0] == '@':
                    user = get_user(split[1][1:])
                    if user is None:
                        self.reply(message, 'Username not found')
                    else:
                        self.reply(message, username(user))
                else:
                    self.reply(message, Default.USERNAME)
            else:
                self.reply(message, Default.USERNAME)

    def campaign_command(self, message):
        if self.check_rate_limit(message):
            c = get_current_campaign()
            if c is None:
                self.reply(message, 'No active campaign')
            else:
                self.reply(message, campaign(c))

    def channel_command(self, message):
        self.reply(message, channel())
