import os
import telebot
import speech_recognition
from pydub import AudioSegment

token = 'my_token'

bot = telebot.TeleBot(token)


def oga2wav(filename):  # Конвертация формата файлов
    new_filename = filename.replace('.oga', '.wav')
    audio = AudioSegment.from_file(filename)

    audio.export(new_filename, format='wav')
    return new_filename


def recognize_speech(oga_filename):  # Перевод голоса в текст + удаление использованных файлов
    wav_filename = oga2wav(oga_filename)
    recognizer = speech_recognition.Recognizer()

    with speech_recognition.WavFile(wav_filename) as source:
        wav_audio = recognizer.record(source)

    text = recognizer.recognize_google(wav_audio, language='ru')

    if os.path.exists(oga_filename):
        os.remove(oga_filename)

    if os.path.exists(wav_filename):
        os.remove(wav_filename)

    return text


def download_file(bot, file_id):  # Скачивание файла, который прислал пользователь
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    filename = file_id + file_info.file_path
    filename = filename.replace('/', '_')

    with open(filename, 'wb') as f:
        f.write(downloaded_file)
    return filename


@bot.message_handler(commands=['start'])
def start_me(message):
    username = message.chat.first_name
    if len(username) > 0:
        bot.send_message(message.chat.id, 'Привет, ' + username + '!')
        sticker = open('hello_sticker.webp', 'rb')
        bot.send_sticker(message.chat.id, sticker)
        sticker.close()
    else:
        bot.send_message(message.chat.id, 'Привет!')
        sticker = open('hello_sticker.webp', 'rb')
        bot.send_sticker(message.chat.id, sticker)
        sticker.close()


@bot.message_handler(commands=['help'])
def help_me(message):
    username = message.chat.first_name
    if len(username) > 0:
        bot.send_message(message.chat.id, username + ', этот бот переводит аудиосообщения в текст!\n'
                                                     'Просто отправьте ему голосовое сообщение.\n'
                                                     'А если вы будете писать гадости, он ответит вам тем же!')
        sticker = open('help_sticker.webp', 'rb')
        bot.send_sticker(message.chat.id, sticker)
        sticker.close()
    else:
        bot.send_message(message.chat.id, 'Этот бот переводит аудиосообщения в текст!\n'
                                          'Просто отправьте ему голосовое сообщение.\n'
                                          'А если вы будете писать гадости, он ответит вам тем же!')
        sticker = open('help_sticker.webp', 'rb')
        bot.send_sticker(message.chat.id, sticker)
        sticker.close()


@bot.message_handler(func=lambda message: True)
def echo_me(message):
    bot.reply_to(message, 'Сам ' + message.text + '!')


@bot.message_handler(content_types=['voice'])
def transcript(message):
    filename = download_file(bot, message.voice.file_id)
    text = recognize_speech(filename)

    bot.send_message(message.chat.id, text)


bot.infinity_polling()
