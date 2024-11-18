# Simple Gemini AI Telegram bot

A simple and unofficial Telegram bot wrapping [Gemini AI API](https://ai.google.dev/), build with [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot)!

Just start a conversation and all messages in the chat will be used as inputs for Gemini AI.

Conversation/context is not stored permanently and will be removed when the bot is restarted.



## Requirements

This bot was built with `Python 3.11`, [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot) and [`generative-ai-python`](https://github.com/google-gemini/generative-ai-python).
Full list of Python requirements is in the `requirements.txt` file, you can use it to install all of them.



## Configuration

Configuration is done through a `.env` file. You can copy example file `.env.example` as `.env` and fill required parameters.

```commandline
cp .env.example .env
```


### Telegram bot

For the bot to work you need:

* [Telegram app API ID and hash](https://telethon-01914.readthedocs.io/en/latest/extra/basic/creating-a-client.html#creating-a-client)
* [Telegram bot token](https://core.telegram.org/bots#creating-a-new-bot)

You can check how to create a bot and access its token [bot token](https://core.telegram.org/bots#creating-a-new-bot).

You can also restrict who can access the bot via `ALLOWED_USERNAMES`.
You can specify multiple usernames delimited by space.
If you don't want to restrict the bot at all you can remove this parameter or leave it empty.

You can also define max response length in characters via `MAX_MESSAGE_LENGTH`.
Bot responses can be up to 4096 characters long, that value is used by default if this parameter is absent.

```dotenv
API_ID='<your secret app API ID>'
API_HASH='<your secret app API hash>'
BOT_TOKEN='<your secret bot token>'
ALLOWED_USERNAMES='@myusername @friendusername'
MAX_MESSAGE_LENGTH=<custom max response length>
```


### Gemini AI API

One required parameter is [API key](https://ai.google.dev/gemini-api/docs/api-key).

```dotenv
GEMINI_API_KEY='<your secret API key>'
```

Through `.env` you can also configure other parameters:
* `GEMINI_MODEL` - which [model](https://ai.google.dev/gemini-api/docs/models/gemini) to use (`gemini-1.5-flash` is used by default)
* `GEMINI_SYSTEM_INSTRUCTION` - [system instruction](https://ai.google.dev/gemini-api/docs/system-instructions?lang=python)

```dotenv
GEMINI_MODEL='gemini-1.5-flash-8b'
GEMINI_SYSTEM_INSTRUCTION='You are a helpful assistant.'
```


## Commands

* `/start` - prints initial message returned from the model for just system message and optional initial message, doesn't impact conversation context
* `/reset` - resets current conversation and removes all context, other than system message


## Running the bot

You can run the bot from the source code directly, or in a Docker container.


### From source code

1. Create a Telegram bot via [BotFather](https://core.telegram.org/bots#6-botfather)
2. Create [Gemini AI API key](https://ai.google.dev/gemini-api/docs/api-key)
3. Install all packages from `requirements.txt`
4. Fill `.env` file
5. Run `main.py` file with Python


### Docker

1. Create a Telegram bot via [BotFather](https://core.telegram.org/bots#6-botfather)
2. Create [Gemini AI API key](https://ai.google.dev/gemini-api/docs/api-key)
3. Fill `.env` file
4. Run `docker compose up -d --build` in terminal

Note that `.env` file is used only for loading environment variables into Docker container through compose.
The file itself isn't added to the container.


## Disclaimer

This bot is in no way affiliated, associated, authorized, endorsed by, or in any way officially connected with Gemini AI or Google.
This is an independent and unofficial project.
Use at your own risk.
