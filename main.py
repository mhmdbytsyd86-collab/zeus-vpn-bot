from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🛒 خرید اشتراک", callback_data="buy"),
            InlineKeyboardButton("📦 سرویس من", callback_data="my_service")
        ],
        [
            InlineKeyboardButton("💳 پرداخت", callback_data="payment"),
            InlineKeyboardButton("🆘 پشتیبانی", callback_data="support")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 سلام!\n\n"
        "به ربات Zeus VPN خوش آمدید.\n"
        "لطفاً یک گزینه را انتخاب کنید:",
        reply_markup=reply_markup
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy":
        await query.edit_message_text(
            "🛒 خرید اشتراک\n\n"
            "لطفاً پلن مورد نظر را انتخاب کنید:\n\n"
            "🥉 یک ماهه - 100GB\n"
            "🥈 سه ماهه - 300GB\n"
            "🥇 شش ماهه - 700GB"
        )

    elif query.data == "my_service":
        await query.edit_message_text(
            "📦 شما هنوز سرویسی ندارید."
        )

    elif query.data == "payment":
        await query.edit_message_text(
            "💳 پرداخت\n\n"
            "شماره کارت بزودی قرار می‌گیرد."
        )

    elif query.data == "support":
        await query.edit_message_text(
            "🆘 پشتیبانی\n\n"
            "پیام خود را ارسال کنید."
        )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

if __name__ == "__main__":
    app.run_polling()
