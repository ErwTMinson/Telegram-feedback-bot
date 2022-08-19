import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import ChatTypeFilter

# Project modubles:
import constants

logging.basicConfig(level=logging.INFO)
bot = Bot(token=constants.TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands = ["self_id"])
async def get_id(message: types.Message):
    await message.reply(f"Your id: {message.from_user.id}")

@dp.message_handler(commands = ['start', 'help'])
async def send_start(message: types.Message):
    await message.reply(constants.HELP)

@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE))
async def feedback(message: types.Message):

    ask_user = -1

    if not message.reply_to_message:

        try:
            ask_user = message.reply_to_message.forward_from.id
        except AttributeError:
            await message.reply("You can\'t send message to feedback.\nGo to settings, in page \"Privacy and Security\", \"forwarded messages\" and set to \"Everybody\"")

    if message.reply_to_message:

        if ask_user != -1:
            await bot.send_message(text = message.text, chat_id = message.reply_to_message.forward_from.id)
        else:
            await message.reply("The user has hidden his ID. He won't be able to answer.")

    elif not message.reply_to_message:
        await bot.forward_message(constants.FEEDBACK_OWNER_ID, message.from_user.id, message.message_id)

    else:
        await message.reply("Wrong type message.")

@dp.message_handler(ChatTypeFilter(chat_type=types.ChatType.PRIVATE), content_types=["photo", "document", "video", "voice", "animation", "sticker"])
async def forward_other_type_message(message: types.Message):
    if not message.reply_to_message:
        await bot.forward_message(constants.FEEDBACK_OWNER_ID, message.from_user.id, message.message_id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=constants.SKIP_UPDATES)
