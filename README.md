
# Discord BirthdayBot

This Discord bot helps servers track their user's birthdays and stores them in MongoDB.

## Using the Bot
This bot can be self hosted or with the use of an online hosting services such as Heroku.

### MongoDB
The bot uses MongoDB to store the users birthdays. 

[This guide](https://www.mongodb.com/developer/how-to/use-atlas-on-heroku/) is useful to follow up until step 5 if you're going to self-host as it tells you how to set up the account and where to get the MongoDB URL.

Continue following the guide if you are planning on using Heroku to host the bot for you. As it lays out some helpful steps in setting the bot up.

### Self-Hosting
When self hosting, you need to include the discord bot token as well as the MongoDB URL in your .env file.

Your .env file should look something like this:
```
token=BOT_TOKEN_HERE
url="MONGODB_URL_HERE"
```
Replace with your bot token and MongoDB URL.

### Online Hosting Services
When using an online hosting service such as Heroku, there will probably be a way for you to store the bot token and MongoDB URL in a secure environment. In Heroku, it is in the settings "config vars." For other hosting services, look up/follow their specific guide on where to store the bot token and MondoDB URL.

### Bot Commands
The bot comes with these following commands:

#### !bday add
````
Usage: !bday add @user MM.DD
Description: Add a user's birthday
````
#### !bday delete
````
Usage: !bday delete @user
Description: Delete a user's birthday
````
#### !bday edit
````
Usage: !bday edit @user MM.DD
Description: Edit a user's birthday to a new birthday
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
#### !bday help
````
Usage: !bday help
Description: Lists all the commands known to the bot and how to use them
````
#### !bday deleteall
````
Usage: !bday deleteall
Description: Deletes all the birthdays stored for the current birthday. 

Only users with administrator priviledges can use this command.
````