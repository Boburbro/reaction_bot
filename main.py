import logging
import time

import flask

import telebot

API_TOKEN = "6714693279:AAGfXhdzMQVDeTLI5JJUcPCOoieKiJS7nUo"

WEBHOOK_HOST = "213.109.204.180"
WEBHOOK_PORT = 8443
WEBHOOK_LISTEN = "0.0.0.0"

WEBHOOK_SSL_CERT = "/etc/ssl/certs/webhook_cert.pem"
WEBHOOK_SSL_PRIV = "/etc/ssl/certs/webhook_pkey.pem"

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)

app = flask.Flask(__name__)


@app.route("/", methods=["GET", "HEAD"])
def index():
    return ""


@app.route(WEBHOOK_URL_PATH, methods=["POST"])
def webhook():
    if flask.request.headers.get("content-type") == "application/json":
        json_string = flask.request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ""
    else:
        flask.abort(403)


@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    bot.reply_to(
        message,
        ("Hi there, I am EchoBot.\n" "I am here to echo your kind words back to you."),
    )


@bot.message_handler(func=lambda message: True, content_types=["text"])
def echo_message(message):
    bot.reply_to(message, message.text)


bot.remove_webhook()

time.sleep(0.1)

bot.set_webhook(
    url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, "r")
)

app.run(
    host=WEBHOOK_LISTEN,
    port=WEBHOOK_PORT,
    ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
    debug=False,
)
