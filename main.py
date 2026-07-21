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

from xui_api import create_vless_user


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

    await update.message.reply_text(
        "👋 سلام!\n\n"
        "به ربات Zeus VPN خوش آمدید.\n"
        "لطفاً یک گزینه را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()


    if query.data == "buy":

        keyboard = [
            [
                InlineKeyboardButton(
                    "🥉 یک ماهه - 100GB",
                    callback_data="payment"
                )
            ],
            [
                InlineKeyboardButton(
                    "🥈 سه ماهه - 300GB",
                    callback_data="payment"
                )
            ],
            [
                InlineKeyboardButton(
                    "🥇 شش ماهه - 700GB",
                    callback_data="payment"
                )
            ]
        ]

        await query.edit_message_text(
            "🛒 انتخاب پلن:\n\n"
            "پلن مورد نظر را انتخاب کنید:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    elif query.data == "payment":

        await query.edit_message_text(
            f"💳 پرداخت\n\n"
            f"شماره کارت:\n"
            f"{CARD_NUMBER}\n\n"
            "بعد از پرداخت عکس رسید را ارسال کنید."
        )


    elif query.data == "my_service":

        await query.edit_message_text(
            "📦 شما هنوز سرویسی ندارید."
        )


    elif query.data == "support":

        await query.edit_message_text(
            "🆘 پشتیبانی\n\n"
            "پیام خود را ارسال کنید."
        )


    elif query.data.startswith("approve_"):

        user_id = query.data.split("_")[1]


        user = create_vless_user()


        if user:

            await context.bot.send_message(
                chat_id=user_id,
                text=(
                    "✅ پرداخت شما تایید شد.\n\n"
                    "🔐 اطلاعات سرویس:\n\n"
                    f"UUID:\n{user['uuid']}\n\n"
                    f"Username:\n{user['email']}"
                )
            )


            await query.edit_message_caption(
                caption="✅ پرداخت تایید شد.\n\n🔗 کاربر در حال ساخت است."
            )


        else:

            await query.edit_message_caption(
                caption="⚠️ خطا در اتصال به پنل 3x-ui"
            )



    elif query.data.startswith("reject_"):

        user_id = query.data.split("_")[1]


        await context.bot.send_message(
            chat_id=user_id,
            text="❌ پرداخت شما رد شد."
        )


        await query.edit_message_caption(
            caption="❌ پرداخت رد شد."
        )




async def receive_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user


    keyboard = [
        [
            InlineKeyboardButton(
                "✅ تایید پرداخت",
                callback_data=f"approve_{user.id}"
            ),

            InlineKeyboardButton(
                "❌ رد پرداخت",
                callback_data=f"reject_{user.id}"
            )
        ]
    ]


    await update.message.reply_text(
        "✅ رسید شما دریافت شد.\n"
        "پس از بررسی اعلام می‌شود."
    )


    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=(
            "📩 رسید پرداخت جدید\n\n"
            f"👤 نام: {user.first_name}\n"
            f"🆔 آیدی: {user.id}\n"
            f"Username: @{user.username}"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )




app = Application.builder().token(BOT_TOKEN).build()


app.add_handler(CommandHandler("start", start))

app.add_handler(
    CallbackQueryHandler(button_handler)
)

app.add_handler(
    MessageHandler(filters.PHOTO, receive_receipt)
)



if __name__ == "__main__":
    app.run_polling()
