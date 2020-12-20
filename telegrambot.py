#!/usr/bin/python3
'''
pip3 install python-telegram-bot --upgrade
'''
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters, MessageHandler
from telegram.ext import InlineQueryHandler, Updater
import logging, os, time
from datetime import datetime
import statusLEDs, Relais, data_analysis
from measure import measure
import RPi.GPIO as GPIO
# Copy emojis from: http://www.unicode.org/emoji/charts/full-emoji-list.html


scaleRatio = 1
numberOfAveragedValues = 10
limit = 0.5
path_txt = " "
path_png = " "


#def commands:
def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name} ' + '😃')

def start(update, context):
    #Starte die Überwachung
    context.bot.send_message(chat_id=update.effective_chat.id, text="""Hi! I am your personal warping assistant! I will stop your print and text you if warping occurs.""")
    date_time = datetime.now().strftime("%y-%m-%d_%H-%M")
    
    #path = os.path.dirname(__file__) + "/Data/" + date_time
    path_txt = 'Data/' + date_time + ".txt"
    path_png = 'Data/' + date_time + ".png"
    try:
        warping = measure(scaleRatio, numberOfAveragedValues, limit, path_txt)
    except:
        GPIO.cleanup()

    if warping:
        #act:
        Relais.statusDrucker("warping")
        statusLEDs.lightLed("warping")
        time.sleep(20)
        Relais.statusDrucker("no_warping")
        #analyse data:
        data_analysis.data_analysis(path_txt= path_txt, path_png= path_png)
        #inform user:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Attention: warping occured! Please check your 3d printer")
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=path_png)


def stop(update, context):
    #Stoppe die Überwachung 
    context.bot.send_message(chat_id=update.effective_chat.id, text="""Bye! \n Warping assistent stopped!""")
    #Ausgabe des Status +
    os.system('sudo reboot now')

def reboot(update, context):
    #Reboote den Raspberry 
    context.bot.send_message(chat_id=update.effective_chat.id, text='Rebooting...')
    os.system('sudo reboot now')

def echo(update, context):
    #Wiederhole unverständliche Nachrichten
    context.bot.send_message(chat_id=update.effective_chat.id, text= 'Kein Befehl fuer: ' + update.message.text)

def statusDruck(update, context):
    #analyse data:
    data_analysis.data_analysis(path_txt= path_txt, path_png= path_png)
    #inform user:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Recent data: ")
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=path_png)

def warping_LED(update, context):
    #Schalte die rote LED an
    statusLEDs.lightLed("warping")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Green LED is turned off!")

def nowarping_LED(update, context):
    #Schalte die gruene LED an
    statusLEDs.lightLed("no_warping")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Green LED is turned on!")

def get_parameter(update, context):
    msg = "limit = " + str(limit) + "\n" + "scale ratio = " + str(scaleRatio) + "\n" +"average of x avlues = " + str(numberOfAveragedValues)
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

#def commands above: 
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


#bot setup:
#updater = Updater(token ='1431428494:AAGlVbkvMhWOkBjUv8q4z1Nz4s93lwXWcf4', use_context=True) #Kai
updater = Updater(token = '1405480476:AAHBt_66kwETu0BYK0Y4mtk07t4LtDEVa9c', use_context=True) #Max
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

get_parameter_handler = CommandHandler('get_parameter', get_parameter, run_async=True)
dispatcher.add_handler(get_parameter_handler)

#Unknown commands handler - add handlers above:
unknown_handler = MessageHandler(Filters.command, unknown, run_async=True)
dispatcher.add_handler(unknown_handler)


#start bot:
updater.start_polling()
updater.idle()

#Boot up Nachricht des Bots:
print("Hi! I am your personal warping assistant!")
