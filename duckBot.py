import os
import asyncio
# minecraft
import discord
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# db = SQLAlchemy()

class DiscordUser(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    timesDucked = db.Column(db.INTEGER, default=1)

    def __repr__(self):
        return '<Task %r>' % self.id

# Contains the classes and functions used to log the duck counts to a file, like a database
import duckLogger

# Adds environment variables
# Will remove load_dotenv() if I host it on Heroku
# load_dotenv()
TOKEN = os.getenv('DUCK_TOKEN')

# print(TOKEN)

client = discord.Client()

intents = discord.Intents.all()
client = discord.Client(intents=intents)


def inDatabase(name, users):
    for user in users:
        if user.name == name:
            return user.id
    return "no user with that name"



@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.content == "!ducks":
        # Can't be called from the devotion channel
        if message.channel.name == "temple":
            return
        send = ""
        users = DiscordUser.query.all()
        # users = duckLogger.getInfo()
        for user in users:
            send = send + f'{user.name} has devoted {user.timesDucked} times\n'
        await message.channel.send(send)

    if message.content == "H":
        await message.channel.send("It's working")

    if message.channel.name == "gaming":
        # If bot sends message, doesn't count
        if message.author == client.user:
            return

        # users = duckLogger.getInfo()
        users = DiscordUser.query.all()
        # for user in users:
        #     print(user.formatReturn())
        # userID = duckLogger.inUserList(message.author.name, users)

        userID = inDatabase(message.author.name)
        print(userID)

        if userID == "no user with that name":
            print("|||||||")
            newUser = DiscordUser(name=message.author.name)
            db.session.add(newUser)
            db.session.commit()


            # user = duckLogger.User(message.author.name, 1)
            # users.append(user)
        else:
            print("-------")
            user = DiscordUser.query.get_or_404(userID)
            user.timesDucked += 1
            db.session.commit()

            # users[userID].timesDucked = int(users[userID].timesDucked) + 1
            # print(users[userID].timesDucked)
        duckLogger.writeInfo(users)
        print('hi')
    else:
        print('hello')

    print(message.content)


client.run(TOKEN)