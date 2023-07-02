from telethon.sync import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.messages import SendMessageRequest, ExportChatInviteRequest
from telethon.tl.types import InputPeerChannel
import time
import random
import string
from utils.timestamp import create_timestamp

api_id = int(input('api_id: '))
api_hash = input('api_hash: ')
phone_number = input('phone_number: ')

loops = int(input('Сколько каналов создать: '))
target_user = input('Имя аккаунта: ')

client = TelegramClient('', api_id, api_hash)
client.start(phone=phone_number)

user = client.get_input_entity(target_user)


def create_chats(i):
    random_symbols = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    chat_title = f'канал {i} {random_symbols}'

    response = client(CreateChannelRequest(
        title=chat_title,
        about=f'Описание {random_symbols}',
        megagroup=False
    ))

    chat_id = response.chats[0].id
    access_hash = response.chats[0].access_hash

    for _ in range(random.randint(2, 5)):
        message_symbols = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        message_sleep_time = random.uniform(2, 5)
        client(SendMessageRequest(
            peer=InputPeerChannel(chat_id, access_hash),
            message=f"Welcome to {message_symbols}!",
            no_webpage=True
        ))
        time.sleep(message_sleep_time)

    client.send_file(InputPeerChannel(chat_id, access_hash), "preview16.jpg", caption="Image")

    invite_link = client(ExportChatInviteRequest(InputPeerChannel(chat_id, access_hash)))

    with open(f'{target_user}_channels.txt', 'a', encoding='utf8') as f:
        f.write(f"[{create_timestamp()}]:{chat_id}:{chat_title}:{invite_link.link}\n")


for i in range(loops):
    sleep_time = random.uniform(5, 10)
    create_chats(i)
    print(f"Канал {i + 1} создан. Задержка на {sleep_time:.2f} секунды.")
    time.sleep(sleep_time)
