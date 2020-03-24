## Fetching data
from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_data(country="total"):
    url = "https://www.worldometers.info/coronavirus/"
    table_data = [[cell.text.strip().strip(':').lower() for cell in row("td")] for row in BeautifulSoup(urlopen(url).read(), features="html.parser")("tr")]
    table_data = table_data[1:]
    for i,countries in enumerate(table_data):
        if len(countries) == 0:
            return None
        if country.lower() == countries[0]:
            return table_data[i]
    return None

def pritify(country="total"):
    td = ["Country", "Total Cases", "New Cases", "Total Deaths", "New Deaths", "Total Recovered", "Active Cases", "Serious Cases", "Tot Cases/1M pop"]
    data = get_data(country)
    if not data:
        return "NOT FOUND"

    final = ""
    for first, second in zip(td, data):
        final += f"{first}: {second}\n"

    final += "\n\n source - ```https://www.worldometers.info/coronavirus/```"
    return final


import logging, os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)



def start(update, context):
    update.message.reply_text('Hi! \nThis bot can give you live stats of corona virus cases.\n\nType /help\n\nAny issue? admin@amanroy.me')

def help(update, context):
    update.message.reply_text('Commands\n\n/help - shows this menu\n/links - shows important links related to corona virus\n/get country_name - shows corona case stats of that country\n/get total - shows total cases across countries')

def links(update, context):
    update.message.reply_text('Here are some important links -\n\nWHO Myth Busters: http://tiny.cc/coronamyth\nCorona information(India): http://tiny.cc/mohfw\nQ&A on coronavirus: http://tiny.cc/qandawho')

def get(update, context):
    update.message.reply_text(pritify(' '.join(update.message.text.split()[1:]).lower()))

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(os.getenv('TOKEN'), use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("links", links))


    dp.add_handler(MessageHandler(Filters.text, get))

    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
