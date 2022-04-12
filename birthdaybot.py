import discord
from discord.ext import commands, tasks
import pymongo
from pymongo import MongoClient
import os
from datetime import date, datetime
# from dotenv import load_dotenv

# load_dotenv()

# reading token from text file
#token = open("token.txt", "r").read()
token = os.getenv("token")
url = os.getenv("url")

client = discord.Client()

cluster = MongoClient(url)
db = cluster["UserData"]
collection = db["UserData"]

@client.event
async def on_ready():
    channel = client.get_channel(918642140379250742)
    print('channel', channel)
    change_status.start(channel)
    print('We have logged in as {0.user}'.format(client))

# loop to get birthday
@tasks.loop(minutes=0.5)
async def change_status(channel):
    today = date.today().strftime("%d.%m")
    # day/month
    print("today's date: ", today)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")[:-3]
    print("Current Time =", current_time)
    results = collection.find({"bday": today})
    for birthday in results:
        name = birthday["name"]
        print("name: ", name)
        if (today == birthday["bday"]):
            message = "@everyone It's " + name + "'s birthday!! \n"
            if (current_time == "02:42"):
                await channel.send(message)
    


@client.event
async def on_message(message):
    # ignore messages from bot itself
    if message.author == client.user:
        return

    # test command
    if message.content.startswith('$bday test'):
        author = str(message.author.id)
        answer = "It's <@" + author + ">'s birthday!!\n"
        await message.channel.send(answer)
    
    if message.content.startswith('$bday setmy'):
        bday = message.content.split('$bday setmy ')[1]
        print(bday)
        post = {"name": message.author.id, "bday": bday}
        # db_key = str(message.author.id)
        # db[db_key] = bday
        collection.insert_one(post)

        answer = 'I set the birthday for you, ' + message.author.name + '!'
        await message.channel.send(answer)

    # setting birthdays for users
    if message.content.startswith('$bday setfor'):
        user = message.content.split('$bday setfor ')[1].split(' ')[0]
        bday = message.content.split('$bday setfor ')[1].split(' ')[1]
        print('user', user)
        print('bday', bday)
        post = {"name": user, "bday": bday}
        collection.insert_one(post)

        answer = 'I set the birthday for ' + user + '!'
        await message.channel.send(answer)

    # getting all the birthdays stored in database
    if message.content.startswith('$bday list'):
        answer = 'All birthdays I know: \n'
        for birthday in collection.find({}).sort('bday', 1):
            name = birthday["name"]
            answer = answer + name + " " + birthday['bday'] + '\n'

        print(answer)
        await message.channel.send(answer)

    # deleting a specific users birthday
    if message.content.startswith('$bday delete'):
        user = message.content.split('$bday delete ')[1].split(' ')[0]
        bday = message.content.split('$bday delete ')[1].split(' ')[1]
        results = collection.find({"name": name})
        if results.count() < 1:
            answer = "There are no birthdays with that name."
            await message.channel.send(answer)
        else:
            collection.delete_one({"name": name})
            await message.channel.send("Birthday deleted")
    
    # deleting all the birthdays stored (mostly for testing)
    if message.content.startswith('$bday removeall'):
        collection.delete_many({})
        await message.channel.send('Deleted all birthdays')

client.run(token)
