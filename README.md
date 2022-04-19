
# Discord BirthdayBot

This Discord bot helps servers track their user's birthdays and stores them in MongoDB.

## Using the Bot
This bot can be self hosted or with the use of an online hosting services such as Heroku.

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

### Online Hosting Services
When using an online hosting service such as Heroku, there will probably be a way for you to store the bot token and MongoDB URL. In Heroku, it is in the settings "config vars." For other hosting services, follow their specific guide on where to store the bot token and MondoDB URL.

### Bot Commands
The bot comes with these following commands:

#### !bday add
````
Usage: !bday add @user DD.MM
Description: Adds users birthday
````
#### !bday delete
````
Usage: !bday delete @user
Description: Deletes user birthday
````
#### !bday list
````
Usage: !bday list
Description: Lists all known birthdays in current server
````
#### !bday test
````
Usage: !bday test
Description: Sends a test message to let people know bot is working
````
#### !bday commands
````
Usage: !bday commands
Description: Lists all the commands known to the bot and how to use them
````
#### !bday deleteall
````
Usage: !bday deleteall
Description: Deletes all the birthdays stored for the current birthday. Only users with administrator priviledges can use this command.
````