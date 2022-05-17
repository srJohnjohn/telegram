import urllib
import json 
import time
import requests
import csv 
from conf.settings import TELEGRAM_TOKEN as TOKEN


URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def arquivo_resposta(id):
    pass

def carregar_Questoes(link):
    lista = []
    with open(link, 'r') as data: 
        for line in csv.reader(data): 
            lista.append(line)
    return lista

def salvar_Respostas(questao, resposta, id):
    arquivo = 'respostasCandidato{}.csv'
    #editar para fica com nome o id do participante
    with open(arquivo.format(id), 'a', newline='') as data:
        whiter = csv.writer(data)
        whiter.writerow([questao[0], resposta])


def iniciar(chat_id):
    questoes = carregar_Questoes("questoes.csv")
    keyboard = build_keyboard()
    last_update_id = None
    print("lendo questoes")
    for questao in questoes:
        #fazer pergunta
        send_message(questao[0], chat_id, keyboard)
        #ler resposta
        #handle_updates(updates)
        updates = get_updates(last_update_id)
        text = None
        print("leu algua coisa")
        for update in updates["result"]:
            print (len(updates["result"]))
            last_update_id = get_last_update_id(updates) + 1
            text = update["message"]["text"]
        salvar_Respostas(questao, text, chat_id)
    
        

def get_url(url):
    print("enviando mesagem")
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

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id, reply_markup=None):
    print(text)
    print(chat_id)
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    # if reply_markup:
    #     url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        if text == "/done":
            keyboard = build_keyboard()
            send_message("Digite /start para começar a prova", chat)
        elif text == "/start":
            keyboard = build_keyboard()
            iniciar(chat)
        elif text.startswith("/"):
            continue

def build_keyboard():
    keyboard = ["sim", "nao"]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)
        
def  main():
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