import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CurrencyConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def help(message):
    bot.send_message(message.chat.id, f"Приветствую, {message.from_user.first_name} {message.from_user.last_name}. \
\nДля начала работы требуется ввести :  \n<Валюту которая у вас есть> \
\n<Валюту в которую вы хотите перевести деньги> \
\n<Количество переводимой валюты>\
\n Для просмотра доступных валют введите команду /values ")

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные Валюты: "
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise ConvertionException("Слишком много значений")

        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя \n{e}")
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {int(total_base) * amount}'
        bot.send_message(message.chat.id, text)


bot.polling()