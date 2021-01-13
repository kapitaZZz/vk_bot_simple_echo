print('Starting BOT..')
stop = False

while not stop:
    try:
        import vk_api
        from vk_api.longpoll import VkEventType, VkLongPoll
        from config import TOKEN
        import time
        import datetime
        from commands import commands_list
        import keyboard

        vk = vk_api.VkApi(token=TOKEN)
        longpoll = VkLongPoll(vk)


        def get_keyboard(path):
            keyboard = open(f"keyboard/{path}.json", "r", encoding="UTF-8").read()
            return keyboard


        def send_hello(user_id):
            send_message(user_id, f'Привет, {get_username(user_id)}', get_keyboard('main'))


        def send_commands(user_id, commands):
            command = '\n'.join(commands)
            send_message(user_id, f'commands allow:\n\n' + str(command), get_keyboard('main'))


        def send_message(user_id, message, keyboard=None):
            vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0, 'keyboard': keyboard})


        def get_username(user_id):
            user_name = vk.method('users.get', {'user_ids': user_id, 'fields': 'first_name'})
            user_name = user_name[0]['first_name']
            return user_name


        def get_user_lastname(user_id):
            user_lastname = vk.method('users.get', {'user_ids': user_id, 'fields': 'first_name'})
            user_lastname = user_lastname[0]['last_name']
            return user_lastname


        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                msg = event.text.lower()
                user_id = event.user_id
                if msg == 'начать':
                    send_hello(user_id)
                elif msg == '/help':
                    send_commands(user_id, commands_list)
                elif msg == '/some_action':
                    pass
                elif msg == '/clear':
                    send_message(user_id, 'keyboard hidden', get_keyboard('clear'))
                elif msg == '/main':
                    send_message(user_id, 'keyboard unhidden', get_keyboard('main'))
                else:
                    send_message(user_id, 'Unknown command, use /help', get_keyboard('main'))

    except Exception as error_msg:
        print(f'Connection failed...wait...Error is {error_msg}')
        time.sleep(5)
        print('...restarting.....')

print('Stopped.')
