#!/usr/bin/python3
'''
pip3 install python-telegram-bot --upgrade
'''
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters, MessageHandler
from telegram.ext import InlineQueryHandler, Updater
import logging, os, time
from datetime import datetime
import statusLEDs, Relais
from measure import measure
from csv import writer

# Copy emojis from: http://www.unicode.org/emoji/charts/full-emoji-list.html

scaleRatio = -1
numberOfAveragedValues = 20
limit = 15000000
date_time = " "

#def commands:
def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name} ' + '😃')

def start(update, context):
    #Starte die Überwachung
    context.bot.send_message(chat_id=update.effective_chat.id, text="""Hi! I am your personal warping assistant! 
    I will stop your print and text you if warping occurs.""")
    
    date_time = datetime.now().strftime("%y_%m_%d_%H_%M") + ".csv"
    path = (os.path.dirname(__file__) + "/Data/" + date_time)
    print("Values are saved to: ", path)
    f = open(path, mode='w+',encoding="utf-8", newline="")
    f_csv_writer = writer(f,delimiter=",")
    f_csv_writer.writerow("row tindex, row time, outputvalue, force")
    
    warping = measure(scaleRatio, numberOfAveragedValues, limit, date_time, f_csv_writer)

    if warping:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Attention: warping occured! Please check your 3d printer")
        statusLEDs.lightLed("warping")
        Relais.statusDrucker("warping")
        time.sleep(20)
        Relais.statusDrucker("no_warping")
        f.close()

def stop(update, context):
    #Stoppe die Überwachung 
    context.bot.send_message(chat_id=update.effective_chat.id, text="""Bye!
                            Warping assistent stopped!""")
    #Ausgabe des Status +
    #os.system('sudo reboot now')

def reboot(update, context):
    #Reboote den Raspberry 
    context.bot.send_message(chat_id=update.effective_chat.id, text='Rebooting...')
    os.system('sudo reboot now')

def echo(update, context):
    #Wiederhole unverständliche Nachrichten
    context.bot.send_message(chat_id=update.effective_chat.id, text= 'Kein Befehl fuer: ' + update.message.text)

def statusDruck(update, context):
    #Sende PNG der Datenauswertung
    context.bot.send_message(chat_id=update.effective_chat.id, text='Recent Data: ')
    #context.bot.send_photo(chat_id=update.effective_chat.id, photo='PfadBild')

def warping_LED(update, context):
    #Schalte die rote LED an
    statusLEDs.lightLed("warping")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Green LED is turned off!")

def nowarping_LED(update, context):
    #Schalte die gruene LED an
    statusLEDs.lightLed("no_warping")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Green LED is turned on!")

'''
def set_limit(update, context):
    #limit = 
    context.bot.send_message(chat_id=update.effective_chat.id, text="Limit is set to " + limit +"N")
'''

def get_limit(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Limit is set to " + limit + "N")


#def commands above: 
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")



#bot setup:
updater = Updater(token ='1431428494:AAGlVbkvMhWOkBjUv8q4z1Nz4s93lwXWcf4', use_context=True)
dispatcher = updater.dispatcher
jobqueque = updater.job_queue

#error logging:
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

#handler:
hello_handler = CommandHandler('hello', hello, run_async=True)
dispatcher.add_handler(hello_handler)

start_handler = CommandHandler('start', start, run_async=True)
dispatcher.add_handler(start_handler)

stop_handler = CommandHandler('stop', stop, run_async=True)
dispatcher.add_handler(stop_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo, run_async=True)
dispatcher.add_handler(echo_handler)

reboot_handler = CommandHandler('reboot', reboot, run_async=True)
dispatcher.add_handler(reboot_handler)

status_handler = CommandHandler('status', statusDruck, run_async=True)
dispatcher.add_handler(status_handler)

warpingLED_handler = CommandHandler('warpingLED', warping_LED, run_async=True)
dispatcher.add_handler(warpingLED_handler)

nowarpingLED_handler = CommandHandler('nowarpingLED', nowarping_LED, run_async=True)
dispatcher.add_handler(nowarpingLED_handler)

'''
setlimit_handler = CommandHandler('set_limit', set_limit)
dispatcher.add_handler(setlimit_handler)
'''

getlimit_handler = CommandHandler('get_limit', get_limit, run_async=True)
dispatcher.add_handler(getlimit_handler)

#Unknown commands handler - add handlers above:
unknown_handler = MessageHandler(Filters.command, unknown, run_async=True)
dispatcher.add_handler(unknown_handler)

#start bot:
updater.start_polling()
updater.idle()

#Boot up Nachricht des Bots:
print("Hi! I am your personal warping assistant!")