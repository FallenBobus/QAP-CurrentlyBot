import telebot
from config import keys, TOKEN
from extensions import APIException, ConvertСurrency
bot = telebot.TeleBot(TOKEN)


# Руководство пользователя
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты>  <в какую валюту перевести> \
<количество переводимой валюты> \nУвидеть список всех достпуных валют: /values'

    bot.reply_to(message, text)


# Список доступных валют для пользователя
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


# Главный обработчик, принимает валюты и число, обрабатывает ошибки, отправляет пользователю
# результат работы
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неправильное количество параметров, ознакомьтесь с руководством: /help')

        base, quote, amount = values
        total_base = ConvertСurrency.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}, сравните с /values')

    else:
        text = f'Цена {amount} {base} в {quote} равна - {total_base*int(amount)}'
        bot.send_message(message.chat.id, text)


bot.polling()
