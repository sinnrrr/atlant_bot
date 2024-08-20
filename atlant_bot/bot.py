import datetime
import shelve
import textwrap

import pytz
from telegram import Update
from telegram.ext import ContextTypes

from atlant_bot.driver import Driver
from atlant_bot.gazovik import Gazovik
from atlant_bot.settings import GAZOVIK_PASSWORD, GAZOVIK_USERNAME, STORAGE_FILENAME

DAILY_TIME = datetime.time(hour=7, minute=30, tzinfo=pytz.timezone("Europe/Kiev"))
DAYS_EFFECTIVE = (1, 2, 3, 4, 5)

driver = Driver(headless=False)
gazovik = Gazovik(driver, GAZOVIK_USERNAME, GAZOVIK_PASSWORD)


def _balance_message(balance: float) -> str:
    return f"Баланс: {balance} грн"


async def send_notification_job(context: ContextTypes.DEFAULT_TYPE):
    balance = gazovik.get_balance()

    with shelve.open(STORAGE_FILENAME) as db:
        for chat_id in db["subscribed"]:
            await context.bot.send_message(
                chat_id=chat_id, text=_balance_message(balance)
            )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat:
        return
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Зачекай, будь ласка..."
    )

    balance = gazovik.get_balance()
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=_balance_message(balance)
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat:
        return

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=textwrap.dedent(
            """\
        Привіт!
        Щоб підписатись на сповіщення про баланс тисни /subscribe 🔔
        Якщо хочеш перевірити баланс зараз, просто напиши /balance 🙂
        """
        ),
    )


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat:
        raise ValueError("Chat is not set")

    with shelve.open(STORAGE_FILENAME) as db:
        current_subscribers = db.get("subscribed", [])
        if update.effective_chat.id in current_subscribers:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=textwrap.dedent(
                    """
                    Ти вже підписаний на сповіщення 🔔
                    Щоб відписатись, тисни /unsubscribe 🔕
                    """
                ),
            )
            return
        current_subscribers.append(update.effective_chat.id)
        db["subscribed"] = current_subscribers
        print(db["subscribed"])

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=textwrap.dedent(
            """
        Ну все.. тепер, ти підписаний на сповіщення 🔔
        Очікуй повідомлення в робочі дні о 8 годині 🙂

        Ти завжди можеш відписатись від сповіщень, для цього потрібно тиснути /unsubscribe 🔕
        """
        ),
    )


async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat:
        raise ValueError("Chat is not set")

    with shelve.open(STORAGE_FILENAME) as db:
        if update.effective_chat.id not in db["subscribed"]:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Ти і не був підписаний на сповіщення 🤓",
            )
            return

        current_subscribers = db["subscribed"]
        current_subscribers.remove(update.effective_chat.id)
        db["subscribed"] = current_subscribers

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=textwrap.dedent(
            """
        Ти відписався від сповіщень 🔕
        Якщо зміниш свою думку, тисни /subscribe 🔔
        """
        ),
    )
