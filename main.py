from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CARD_NUMBER = os.getenv("CARD_NUMBER")

ADMIN_ID = 5769833164


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
            "🥉 یک ماهه - 100GB\n"
            "🥈 سه ماهه - 300GB\n"
            "🥇 شش ماهه - 700GB\n\n"
            "بعد از انتخاب پلن، از بخش 💳 پرداخت استفاده کنید."
        )

    elif query.data == "my_service":
        await query.edit_message_text(
            "📦 شما هنوز سرویسی ندارید."
        )

    elif query.data == "payment":
        await query.edit_message_text(
            f"💳 پرداخت\n\n"
            f"شماره کارت:\n"
            f"{CARD_NUMBER}\n\n"
            "بعد از پرداخت، لطفاً عکس رسید را ارسال کنید."
        )

    elif query.data == "support":
        await query.edit_message_text(
            "🆘 پشتیبانی\n\n"
            "پیام خود را ارسال کنید."
        )


# دریافت رسید پرداخت
async def receive_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    await update.message.reply_text(
        "✅ رسید شما دریافت شد.\n"
        "پس از بررسی، نتیجه اعلام می‌شود."
    )

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=(
            "📩 رسید پرداخت جدید\n\n"
            f"👤 نام: {user.first_name}\n"
            f"🆔 آیدی: {user.id}\n"
            f"👤 Username: @{user.username}"
        )
    )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

# دریافت عکس رسید
app.add_handler(MessageHandler(filters.PHOTO, receive_receipt))


if __name__ == "__main__":
    app.run_polling()
