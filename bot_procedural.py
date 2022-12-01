import time
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from vkbot import VkBot


def write_msg(user_id, msg):
    vk.method('messages.send', {'user_id': user_id, 'random_id': int(time.time()), 'message': msg})


# API-ключ
token = ""

# Id группы
group_id = 202629377

# Авторизация как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообществом
longpoll = VkLongPoll(vk)

# Основной цикл
print("Server started")
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            print('New message:')
            print(f'For me by: {event.user_id}')

            bot = VkBot(event.user_id)
            write_msg(event.user_id, bot.new_message(event.text))

            print('Text: ', event.text)

