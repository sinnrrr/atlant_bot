import logging

from telegram.ext import Application, CommandHandler

from atlant_bot.bot import (
    DAILY_TIME,
    DAYS_EFFECTIVE,
    balance,
    send_notification_job,
    start,
    subscribe,
    unsubscribe,
)
from atlant_bot.settings import BOT_TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


if __name__ == "__main__":
    application = Application.builder().token(BOT_TOKEN).build()
    if not application.job_queue:
        raise ValueError("Job queue is not set")

    application.job_queue.run_daily(
        send_notification_job,
        time=DAILY_TIME,
        days=DAYS_EFFECTIVE,
        data=[],
    )

    application.add_handlers(
        [
            CommandHandler("start", start),
            CommandHandler("subscribe", subscribe),
            CommandHandler("unsubscribe", unsubscribe),
            CommandHandler("balance", balance),
        ]
    )
    application.run_polling()
