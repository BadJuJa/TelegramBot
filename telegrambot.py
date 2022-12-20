# -*- coding: utf-8 -*-

from requests.structures import CaseInsensitiveDict
import telebot
import requests
API_KEY = '5854112341:AAFRlN12UK2_K57VE6P5Crc-1mcsuYKsS40'

POST_URLS = {
    'Fantasy Name': 'https://randomall.ru/api/general/fantasy_name',
    'Plot': 'https://randomall.ru/api/general/plot',
    'Saying': 'https://randstuff.ru/saying/generate/',
}

bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, 'Бот-генератор (почти). Используй /comands чтобы увидеть список команд')


@bot.message_handler(commands=['comands'])
def comands(message):
    out = '/plot - идея для сюжета\n/name - странное имя\n/saying - мудрость'
    bot.send_message(message.chat.id, out)


@bot.message_handler(commands=['plot'])
def plot(message):
    r = requests.post(POST_URLS['Plot'])
    bot.send_message(message.chat.id, r.text)


@bot.message_handler(commands=['name'])
def fantasy_name(message):
    r = requests.post(POST_URLS['Fantasy Name'])
    out = list(map(str.strip, r.text.replace('<br>', ' ').replace(
        '"', '').replace('  ', ' ') .split(' ')))
    try:
        bot.send_message(message.chat.id, out[0])  # '\n'.join(out))
    except:
        bot.send_message(message.chat.id, out[1])


@bot.message_handler(commands=['saying'])
def saying(message):
    headers = CaseInsensitiveDict()
    headers["x-requested-with"] = "XMLHttpRequest"
    r = requests.post(POST_URLS['Saying'], headers=headers).json()['saying']
    saying = r['text']
    author = r['author']
    out = saying + '\n(c) ' + author
    bot.send_message(message.chat.id, out)


bot.polling(none_stop=True)
