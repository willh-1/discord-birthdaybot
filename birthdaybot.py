import discord
from discord.ext import commands, tasks
import pymongo
from pymongo import MongoClient
import os
from datetime import date, datetime

# uncomment for self hosting, needed to load token and url from .env
from dotenv import load_dotenv
load_dotenv()

# reading token and mongodb url from heroku config vars or from .env if self hosting
token = os.getenv("token")
url = os.getenv("url")

client = commands.Bot(command_prefix = "!bday ", help_command = None)

# MongoDB connection
cluster = MongoClient(url)
db = cluster["UserData"]
collection = db["UserData"]

@client.event
async def on_ready():
    # Changes bot presences to "listening to !bday help"
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name = "!bday help"))
    change_status.start()
    print("We have logged in as {0.user}".format(client))

# loops every minute to check the time of day
# grabs the birthdays in database that are current date
# for each birthday, the channelID stored will be the channel that the birthday announcement will be made
# announces the message at 16:00 UTC if there is a birthday today
@tasks.loop(minutes=1)
async def change_status():
    today = date.today().strftime("%m.%d")
    print("today's date: ", today)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")[:-3]
    print("Current Time =", current_time)
    # Check in database for birthdays that are for current day
    results = collection.find({"bday": today})
    for birthday in results:
        name = birthday["name"]
        channel = client.get_channel(birthday["channelID"])
        print("name: ", name)
        print("channel: ", channel)
        if (today == birthday["bday"]):
            message = "@everyone It's " + name + "'s birthday!! <:feelsbirthdayman:478595418620690446>\n"
            # announce at 16:00 UTC
            if (current_time == "16:00"):
                emoji = '<:feelsbirthdayman:478595418620690446>'
                bdaymsg = await channel.send(message)
                await bdaymsg.add_reaction(emoji)

# function that ensures date inputted follows format: MM.DD
def is_valid_date(bday):
    try:
        # ensures birthday includes zero-padded numbers. ie 01.01 vs 1.1
        if bday != datetime.strptime(bday, "%m.%d").strftime("%m.%d"):
            raise ValueError
        return True
    except ValueError:
        return False     

# command to add a user's birthday
@client.command()
async def add(ctx, user, bday):
    if is_valid_date(bday) == False:
        message = "Incorrect birthday format. Correct format is: MM.DD"
        await ctx.channel.send(message)
    # users birthday already exists in db
    # user can be in other servers that also has this bot, should be able to save birthdays to that server aswell
    elif (collection.count_documents({"name": user})) and (collection.count_documents({"serverID": ctx.guild.id}))  == 1 :
        message = user + "'s birthday already exists"
        await ctx.channel.send(message)
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
    result_count = collection.count_documents({"name": user, "serverID": ctx.guild.id})
    # user not found in db
    if result_count < 1:
        message = "That user has no birthdays stored."
        await ctx.channel.send(message)
    else:
        collection.delete_one({"name": user})
        await ctx.channel.send("Birthday deleted")

# command that edits a users birthday
@client.command()
async def edit(ctx, user, bday):
    result_count = collection.count_documents({"name": user, "serverID": ctx.guild.id})
    if result_count < 1:
        message = "That user has no birthdays stored"
        await ctx.channel.send(message)
    elif is_valid_date(bday) == False:
        message = "Incorrect birthday format. Correct format is: MM.DD"
        await ctx.channel.send(message)
    else:
        collection.update_one({"name": user, "serverID": ctx.guild.id}, {"$set":{"bday": bday}})
        message = "Users birthday has been updated."
        await ctx.channel.send(message)

# command that lists all the birthdays known
@client.command()
async def list(ctx):
    message = "All birthdays I know: \n"
    result = collection.find({"serverID": ctx.guild.id}).sort("bday") 
    for birthday in result:
        name = birthday["name"]
        message = message + name + " " + birthday["bday"] + "\n"
    print(message)
    await ctx.channel.send(message)

# command to test that bot works
@client.command()
async def test(ctx):
    author = str(ctx.author.id)
    message = "@everyone It's <@" + author + ">'s birthday!! <:feelsbirthdayman:478595418620690446>\n"
    emoji = '<:feelsbirthdayman:478595418620690446>'
    bdaymsg = await ctx.channel.send(message)
    await bdaymsg.add_reaction(emoji)

# command to bring up all commands bot knows
@client.command()
async def help(ctx):
    embed = discord.Embed(
        title = "All available commands:",
        color = discord.Colour.blue()
    )
    embed.add_field(name="!bday add @user MM.DD", value="Add a users birthday", inline=False)
    embed.add_field(name="!bday delete @user ", value="Delete a users birthday", inline=False)
    embed.add_field(name="!bday edit @user MM.DD", value="Edit a users birthday", inline=False)
    embed.add_field(name="!bday list", value="Lists all known birthdays", inline=False)
    embed.add_field(name="!bday test", value="Sends a test message", inline=True)
    embed.add_field(name="!bday help", value="Brings up this list of commands", inline=False)
    embed.add_field(name="!bday deleteall", value="Deletes all known birthdays in server. \nONLY ADMINS CAN USE THIS", inline=False)
    
    await ctx.send(embed=embed)

# command to delete all birthdays from db (mostly for testing)
@client.command()
async def deleteall(ctx):
    # checks that person using command has administrator priviledges
    if ctx.message.author.guild_permissions.administrator:
        # only deletes birthdays from that specific discord server
        collection.delete_many({"serverID": ctx.guild.id})
        await ctx.channel.send('All birthdays have been deleted')
    else:
        await ctx.channel.send('Only admins are allowed to delete all')

client.run(token)
