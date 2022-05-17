from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv

from conf.settings import TELEGRAM_TOKEN as TOKEN
from conf.settings import API_ID, API_HASH, PHONE

client = TelegramClient(PHONE, API_ID, API_HASH)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(PHONE)
    client.sign_in(PHONE, input('Enter the code: '))


chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0,
         ))
chats.extend(result.chats)

for chat in chats:
    try:
        #if chat.megagroup== True:
        groups.append(chat)
    except:
        continue


print('Choose a group to scrape members from:')
i=0
for g in groups:
    print(str(i) + '- ' + g.title)
    i+=1

g_index = input("Enter a Number: ")
target_group=groups[int(g_index)]

mensagens_grupo = client.get_messages(target_group, limit=20)
print(mensagens_grupo)

mensagens = []
for m in mensagens_grupo:
    mensagens.append(m.message)
print(mensagens[0].message)

# print(mensagens)

# print('Choose a group to send message:')
# i=0
# for g in groups:
#     print(str(i) + '- ' + g.title)
#     i+=1

# g_index_send = input("Enter a Number: ")
# target_group_send=groups[int(g_index_send)]

# for s in mensagens:
#     print(s)
#     if s != '':
#         client.send_message(target_group_send.id, s)  