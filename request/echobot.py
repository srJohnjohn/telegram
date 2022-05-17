import urllib
import json 
import time
import requests

from conf.settings import TELEGRAM_TOKEN as TOKEN
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
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


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
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

def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)

def texto_da_opcao(opcao):
    if opcao == '0' or opcao == 'menu':
        return f'''Olá bem vindo a nossa lanchonete Digite o número do hamburguer gostaria de pedir:
        1 - Queijo quente
        2 - cheseBurger com Bacon 
        3 - dupro cheseburger'''
    if opcao == '1':
        return f'''Queijo quente - R$5,00 Confirmar pedido?(s/n)'''
    elif opcao == '2':
        return f'''cheseBurger com Bacon - R$15,00 Confirmar pedido?(s/n)'''
    elif opcao == '3':
        return f'''dupro cheseburger - R$20,00 Confirmar pedido?(s/n)'''
    elif opcao.lower() in ('s', 'sim'):
        return ''' Pedido Confirmado! '''
    elif opcao.lower() in ('n', 'não'):
        return ''' Pedido Confirmado! '''
    else:
        return 'Gostaria de acessar o menu? Digite "menu"'


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()