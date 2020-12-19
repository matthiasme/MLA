from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters, MessageHandler
from telegram.ext import InlineQueryHandler, Updater
import logging

#def commands:
def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name} ' + '😃')

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def callback_alarm(context: CallbackContext):
    context.bot.send_message(chat_id=context.job.context, text='BEEP')

def dog(update, context):
    context.bot.send_photo(chat_id=update.effective_chat.id, photo='https://dog.ceo/api/breeds/image/random')

#def commmands above:
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

#inline:
def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

#queque:
def callback_minute(context: CallbackContext):
    context.bot.send_message(chat_id='@examplechannel', 
                             text='One message every minute')

def callback_30(context: CallbackContext):
    context.bot.send_message(chat_id='@examplechannel', 
                             text='A single message with 30s delay')

def callback_timer(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text='Setting a timer for 1 minute!')

    context.job_queue.run_once(callback_alarm, 60, context=update.message.chat_id)

#setup:
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
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler, run_async=True)
caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler, run_async=True)
inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler, run_async=True)
dog_handler = CommandHandler('dog', dog)
dispatcher.add_handler(dog_handler)

#queque execution:
#job_minute = j.run_repeating(callback_minute, interval=60, first=0)
#j.run_once(callback_30, 30)
timer_handler = CommandHandler('timer', callback_timer)
updater.dispatcher.add_handler(timer_handler)

#add handlers above:
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

#start bot:
updater.start_polling()
updater.idle()