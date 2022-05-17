import urllib
import json 
import time
import requests
from dbhelper import DBHelper
from conf.settings import TELEGRAM_TOKEN as TOKEN

db = DBHelper()

URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def cardapio():
    itens = ["1 - Queijo quente",
        "2 - chesseBurger com Bacon" ,
        "3 - dupro cheseburger",]
    return itens

def get_url(url):
    print(url)
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

 
def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        items = db.get_items(chat)
        if text == "/done":
            keyboard = build_keyboard(items)
            send_message("Select an item to delete", chat, keyboard)
        elif text == "/start":
            keyboard = build_keyboard(cardapio())
            send_message(f'''Olá bem vindo a nossa lanchonete Digite o número do hamburguer gostaria de pedir:''', chat, keyboard)
        elif text.startswith("/"):
            continue
        elif text == "1 - Queijo quente":
            db.add_item(text, chat)
            send_message(f'''Queijo quente - R$5,00 Confirmar pedido?(s/n)''', chat)
        elif text == "2 - chesseBurger com Bacon":
            db.add_item(text, chat)
            send_message(f'''cheseBurger com Bacon - R$15,00 Confirmar pedido?(s/n)''', chat)
        elif text == "3 - dupro cheseburger":
            db.add_item(text, chat)
            send_message(f'''dupro cheseburger - R$20,00 Confirmar pedido?(s/n)''', chat)
        elif text.lower() in ('s', 'sim'):
            db.add_item(text, chat)
            send_message(''' Pedido Confirmado! ''', chat)
        elif text.lower() in ('n', 'não'):
            db.add_item(text, chat)
            send_message(''' Pedido Negado! ''', chat)
        else:
            send_message('Gostaria de acessar o menu? Digite /start', chat)

def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)

def main():
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            print (len(updates["result"]))
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()