from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ChatMemberStatus
import os

BOT_TOKEN = "8944114332:AAHRZZ3-mjkrJwSW2AEjJD0vqzbFr-rSFjA"

CHANNEL_USERNAME = "@s1rluffyera"
CHANNEL_LINK = "https://t.me/s1rluffyera"
OWNER = "@anish_khxtri"
FILE_NAME = "𝐂𝐎𝐖𝐆𝐈𝐑𝐋.py"


async def joined(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in [
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,
        ]
    except:
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ok = await joined(context.bot, update.effective_user.id)

    if not ok:
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
            [InlineKeyboardButton("✅ I Joined", callback_data="check")]
        ]
        await update.message.reply_text(
            "⚠️ Pehle channel join karo.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    keyboard = [
        [InlineKeyboardButton("👤 Owner", callback_data="owner")],
        [InlineKeyboardButton("📁 Files", callback_data="files")]
    ]

    await update.message.reply_text(
        "Welcome!\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    ok = await joined(context.bot, query.from_user.id)

    if not ok:
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
            [InlineKeyboardButton("✅ I Joined", callback_data="check")]
        ]
        await query.message.reply_text(
            "⚠️ Join channel first.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    if query.data == "check":
        keyboard = [
            [InlineKeyboardButton("👤 Owner", callback_data="owner")],
            [InlineKeyboardButton("📁 Files", callback_data="files")]
        ]
        await query.message.reply_text(
            "✅ Verified!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "owner":
        await query.message.reply_text(f"Owner: {OWNER}")

    elif query.data == "files":
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "rb") as f:
                await context.bot.send_document(
                    chat_id=query.message.chat.id,
                    document=f,
                    filename=FILE_NAME,
                    caption="Fast hi2 file"
                )
        else:
            await query.message.reply_text("❌ File not found.")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

print("Bot Running...")
app.run_polling()