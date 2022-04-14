import discord
from discord.ext import commands, tasks
import pymongo
from pymongo import MongoClient
import os
from datetime import date, datetime

# uncomment for local testing loading token and url from .env
from dotenv import load_dotenv
load_dotenv()

# reading token and mongodb url from heroku config vars or from .env if self hosting
token = os.getenv("token")
url = os.getenv("url")

# client = discord.Client()
client = commands.Bot(command_prefix = '$bday ')

cluster = MongoClient(url)
db = cluster["UserData"]
collection = db["UserData"]

@client.event
async def on_ready():
    #channel = client.get_channel(481316592475701248)
    #print('channel', channel)
    change_status.start()
    print('We have logged in as {0.user}'.format(client))

# loop to get birthday
@tasks.loop(minutes=1)
async def change_status():
    today = date.today().strftime("%d.%m")
    # day/month
    print("today's date: ", today)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")[:-3]
    print("Current Time =", current_time)
    results = collection.find({"bday": today})
    for birthday in results:
        name = birthday["name"]
        channel = client.get_channel(birthday["channelID"])
        print("name: ", name)
        print("channel: ", channel)
        if (today == birthday["bday"]):
            message = "@everyone It's " + name + "'s birthday!! \n"
            # announce at 16:00 UTC
            if (current_time == "16:00"):
                await channel.send(message)

# command to add a user's birthday
@client.command()
async def add(ctx, user, bday):
    message = ""
    if len(bday) < 5:
        message = "Incorrect birthday format: DD.MM"
        await ctx.channel.send(message)
    # users birthday already exists in db
    # user can be in other servers that also has this bot, should be able to save birthdays to that server aswell
    elif (collection.count_documents({"name": user})) and (collection.count_documents({"serverID": ctx.guild.id}))  == 1 :
        await ctx.channel.send(user + "'s birthday already exists")
    else:
        post = {
            "name": user,
            "bday": bday,
            "serverID": ctx.guild.id,
            "channelID": ctx.channel.id
        }
        collection.insert_one(post)
        print("Birthday added")
        await ctx.channel.send(user + "'s birthday was added")
    
# command to delete a user's birthday
@client.command()
async def delete(ctx, user):
    # user = message.content.split('$bday delete ')[1].split(' ')[0]
    result_count = collection.count_documents({"name": user})
    # user not found in db
    if result_count < 1:
        answer = "There are no birthdays with that name."
        await ctx.channel.send(answer)
    else:
        collection.delete_one({"name": user})
        await ctx.channel.send("Birthday deleted")

# command that lists all the birthdays known
@client.command()
async def list(ctx):
    message = 'All birthdays I know: \n'
    # print(collection.find({}).sort('bday', 1))
    for birthday in collection.find({"serverID": ctx.guild.id}).sort('bday', 1):
        name = birthday["name"]
        message = message + name + " " + birthday['bday'] + '\n'

    print(message)
    await ctx.channel.send(message)

# command to test that bot works
@client.command()
async def test(ctx):
    author = str(ctx.author.id)
    answer = "It's <@" + author + ">'s birthday!!\n"
    await ctx.channel.send(answer)

# command to delete all birthdays from db (mostly for testing)
@client.command()
async def deleteall(ctx):
    # checks that person using command is an admin
    if ctx.message.author.guild_permissions.administrator:
        collection.delete_many({})
        await ctx.channel.send('All birthdays have been deleted')
    else:
        await ctx.channel.send('Only admins are allowed to delete all')

""" @client.event
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
        result_count = collection.count_documents({"name": user})
        if result_count < 1:
            answer = "There are no birthdays with that name."
            await message.channel.send(answer)
        else:
            collection.delete_one({"name": user})
            await message.channel.send("Birthday deleted")
    
    # deleting all the birthdays stored (mostly for testing)
    if message.content.startswith('$bday removeall'):
        collection.delete_many({})
        await message.channel.send('Deleted all birthdays')
 """
client.run(token)
