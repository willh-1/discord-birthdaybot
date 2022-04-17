
# Discord Python BirthdayBot

This Discord bot helps servers track their user's birthdays and store them in MongoDB.

## Getting Started
This bot can be self hosted or with the use of online hosting services such as Heroku.

### MongoDB
The bot uses MongoDB to store the users birthdays. 

[This guide](https://www.mongodb.com/developer/how-to/use-atlas-on-heroku/) is useful to follow up until step 5 if you wish to self-host to grab the URL. Continue following the guide if you are planning on using Heroku to host the bot for you.

### Self-Hosting
When self hosting there are comments that need to be uncommented so that your bot token and MongoDB URL is readable from your .env file.

Inside your .env file should have:
```
token=BOT_TOKEN_HERE
url="MONGODB_URL_HERE"
```

### Online Hosting
When using an online hosting service, there will probably be a way for you to store the bot token and MongoDB URL such as Heroku's "config vars." Follow the specific hosting services documents on where to store the bot token and MondoDB URL.