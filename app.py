from urllib.request import urlopen
from bs4 import BeautifulSoup

# Helper function for parsing data
def get_country_data(country):
    url = "https://www.worldometers.info/coronavirus/"
    contents = BeautifulSoup(urlopen(url).read(), \
        features="html.parser")

    table_data = [[cell.text.strip().strip(':').lower() \
        for cell in row("td")] for row in contents("tr")]
    table_data = table_data[1:]
    for i,countries in enumerate(table_data):
        if len(countries) == 0:
            return None
        if country.lower() == countries[0]:
            return table_data[i]
    return None

def pritify_country(country):
    columns = ["Country", "Total Cases", "New Cases", \
        "Total Deaths", "New Deaths", "Total Recovered", \
        "Active Cases", "Serious Cases", "Tot Cases/1M pop"]
    data = get_country_data(country)
    if not data:
        return "NOT FOUND"
    final = ""
    for first, second in zip(columns, data):
        final += f"{first}: {second}\n"
    final += "\n\nsource - https://www.worldometers.info/coronavirus/"
    return final

def get_state_data(state):
    url = "https://www.mohfw.gov.in"
    contents = BeautifulSoup(urlopen(url).read(), \
        features="html.parser")

    table_data = [[cell.text.strip().strip(':').lower() \
        for cell in row("td")] for row in contents("tr")]
    final = []
    i = len(table_data) - 1
    while i >= 0:
        if len(table_data[i]) == 0:
            break
        final.append(table_data[i])
        i -= 1
    final.pop(0)

    [j.pop(0) for j in final]

    for i,s in enumerate(final):
        if s[0].lower() == state:
            return final[i]
    return None

def pritify_india(state):
    columns = ["State","Confirmed cases(Indian)",\
        "Confirmed cases(Foreign)", "Cured", "Death"]
    data = get_state_data(state)
    if not data:
        return "Not found"
    final = ""
    for first, second in zip(columns, data):
        final += f"{first}: {second}\n"
    final += "\n\nsource - https://www.mohfw.gov.in"
    return final


# Telegram bot configs
import logging, os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text('Hi! \nThis bot can give you live '\
        'stats of corona virus cases.\n\nType /help\n\nAny issue? ' \
        'admin@amanroy.me')

def help(update, context):
    update.message.reply_text('Commands\n\n/help - shows this ' \
        'menu\n/links - shows important links related to corona ' \
        'virus\n/get country_name - shows corona case stats of ' \
        'that country\n/get total - shows total cases across ' \
        'countries\n/india state_name - Show stats related to that state')

def links(update, context):
    update.message.reply_text('Here are some important links ' \
        '-\n\nWHO Myth Busters: http://tiny.cc/coronamyth\nCorona ' \
        'information(India): http://tiny.cc/mohfw\nQ&A on ' \
        'coronavirus: http://tiny.cc/qandawho')

def get(update, context):
    user_says = " ".join(context.args)
    update.message.reply_text(pritify_country(user_says.lower()))

def india(update, context):
    user_says = " ".join(context.args)
    update.message.reply_text(pritify_india(user_says.lower()))

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(os.getenv('TOKEN'), use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("links", links))
    dp.add_handler(CommandHandler("india", india))
    dp.add_handler(CommandHandler("get", get))

    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()