from telebot import types, TeleBot
from threading import Thread
from converter import convert

bot = TeleBot('5889078300:AAF_Lp705NJ8fnVLagJHuwvYJ693RoDEhRw')
user_queue = {}
queue_place = {}
main_queue = []


@bot.message_handler(content_types=['photo'])
def photo(message: types.Message):
    """Get the photo from user and add it to the user_queue"""
    id = message.from_user.id
    path = bot.get_file(message.photo[-1].file_id).file_path
    chat_id = message.chat.id
    mess_id = bot.send_message(message.chat.id, f'Added to the queue').id
    request = (path, chat_id, mess_id, message.id)
    if id in user_queue:
        user_queue[id].append(request)
    else:
        user_queue[id] = [request]
        main_queue.append(id)
        bot.edit_message_text(f'You are {len(main_queue)} in the queue', chat_id, mess_id)


def main():
    """Converts images from the queue"""
    while True:
        if len(main_queue):
            id = main_queue.pop(0)
            path, chat_id, mess_id, user_mess = user_queue[id].pop(0)
            img = bot.download_file(path)
            with open("img.jpg", 'wb') as file:
                file.write(img)
            for percent in convert():
                bot.edit_message_text(f'Converting... {percent}%', chat_id, mess_id)
            bot.delete_message(chat_id, mess_id)
            with open('res.jpg', 'rb') as file:
                img = file.read()
                bot.send_photo(chat_id, img, has_spoiler=False)
            if len(user_queue[id]):
                main_queue.append(id)
            else:
                user_queue.pop(id)
            for i, v in enumerate(main_queue):
                bot.edit_message_text(f'You are {i + 1} in queue', user_queue[v][0][1], user_queue[v][0][2])


thread = Thread(target=main)
thread.start()
print('bot started...')
bot.polling(none_stop=True)
thread.join()
