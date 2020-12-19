#!/usr/bin/python3
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters, MessageHandler
from telegram.ext import InlineQueryHandler, Updater
import logging, os, time
import execute, statusLEDs, Relais

scaleRatio = -1
numberOfAveragedValues = 20
limit = 15

#def commands:
def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name} ' + '😃')

def start(update, context):
	#Starte die Überwachung
    context.bot.send_message(chat_id=update.effective_chat.id, text="""Hi! I am your personal warping assistant! 
							I will stop your print and text you if warping occurs.""")
		if execute.measure(scaleRatio, numberOfAveragedValues, limit):
			context.bot.send_message(chat_id=update.effective_chat.id, 
									text="Attention: warping occured! Please check your 3d printer")
			statusLEDs.lightLed("warping")
			Relais.statusDrucker("warping")
			time.sleep(20)
			Relais.statusDrucker("no_warping")

def stop(update, context):
	#Stoppe die Überwachung 
    context.bot.send_message(chat_id=update.effective_chat.id, text="""Bye!
							Warping assistent stoped!""")
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
	#Sende PNG der Datenauswertung
    #context.bot.send_photo(chat_id=update.effective_chat.id, photo='PfadBild')

def warping_LED(update, context):
	#Schalte die rote LED an
	statusLEDs.lightLed("warping")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Red LED is turned on!")

def nowarping_LED(update, context):
	#Schalte die gruene LED an
    statusLEDs.lightLed("no_warping")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Green LED is turned off!")

def set_limit(update, context):
	#limit = 
    context.bot.send_message(chat_id=update.effective_chat.id, text="Limit is set to " + limit)

def get_limit(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="Limit is set to " + limit)
		
#setup:
updater = Updater(token ='1431428494:AAGlVbkvMhWOkBjUv8q4z1Nz4s93lwXWcf4', use_context=True)
dispatcher = updater.dispatcher
jobqueque = updater.job_queue

#error logging:
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

#Bot Objekt wird erstellt und diesem werden die Befehle uebergeben
bot = telepot.Bot('1405480476:AAHBt_66kwETu0BYK0Y4mtk07t4LtDEVa9c') #Token
MessageLoop(bot, handle).run_as_thread()

#handler:
hello_handler = CommandHandler('hello', hello)
dispatcher.add_handler(hello_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

stop_handler = CommandHandler('stop', stop)
dispatcher.add_handler(stop_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

reboot_handler = CommandHandler('reboot', reboot)
dispatcher.add_handler(reboot_handler)

status_handler = CommandHandler('status', statusDruck)
dispatcher.add_handler(status_handler)

warpingLED_handler = CommandHandler('warpingLED', warping_LED)
dispatcher.add_handler(warpingLED_handler)

nowarpingLED_handler = CommandHandler('nowarpingLED', nowarping_LED)
dispatcher.add_handler(nowarpingLED_handler)

setlimit_handler = CommandHandler('set_limit', set_limit)
dispatcher.add_handler(setlimit_handler)

getlimit_handler = CommandHandler('get_limit', get_limit)
dispatcher.add_handler(getlimit_handler)

#Unknown commands handler - add handlers above:
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

#start bot:
updater.start_polling()
updater.idle()

#Boot up Nachricht des Bots:
print("Hi! I am your personal warping assistant!")