from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import logging
from groq import Groq

load_dotenv()
TOKEN = os.getenv("TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "mixtral-8x7b-32768"  # You can change this to the Groq model you want to use

# Initialize bot 
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)

class Reference:
    def __init__(self) -> None:
        self.response = ""

reference = Reference()

def clear_past():
    reference.response = ""

@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")

@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start` command
    """
    await message.reply("Hi\nI am a Chat Bot! Created by Bappy. How can I assist you?")

@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm a bot created by Bappy! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)

@dispatcher.message_handler()
async def main_bot(message: types.Message):
    """
    A handler to process the user's input and generate a response using the Groq API.
    """
    print(f">>> USER: \n\t{message.text}")

    chat_completion = groq_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "assistant", "content": reference.response},
            {"role": "user", "content": message.text}
        ]
    )
    
    reference.response = chat_completion.choices[0].message.content
    print(f">>> Groq: \n\t{reference.response}")
    await bot.send_message(chat_id=message.chat.id, text=reference.response)

if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)