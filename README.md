# BrandoBot

Hobby project discord bot to play music in voice channels

## Requirements

### Packages
* Python3
* Discord
* Python-Dotenv
* Youtube_dl
* PyNaCl

### System Requirements
FFmpeg is required for the bot to play music. Simply install from https://www.ffmpeg.org/ for the system the bot is running on. When running on a Windows machine you will need to add the directory "ffmpeg/bin" to the PATH variable.

## Installation
* First ensure FFmpeg is installed correctly wit the command `ffmpeg --version`. If the command is recognized you're all set.
* Install all the packages `pip install -r requirements.txt`
* Create a new file called `.env`, within this file set your discord bot token `DISCORD_TOKEN=your_token`.
* Starting the bot is a smiple as `python bot.py`!
