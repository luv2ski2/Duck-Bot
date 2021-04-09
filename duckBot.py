import os
import asyncio
# minecraft
import discord
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# CTRL + SHIFT + P to open command line, sql open test.db

Base = declarative_base()

DATABASE = os.getenv("DATABASE_URL")

class DiscordUser(Base):
    __tablename__ = "discorduser"

    id = Column('id', Integer, primary_key=True)
    name = Column('username', String)
    timesDucked = Column('timesDucked', Integer, default = 1)


# engine = create_engine('sqlite:///users.db', echo=True)
engine = create_engine(DATABASE, echo=False)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

session = Session()

# user = DiscordUser()
# user.name = "Tester"

# session.add(user)
# session.commit()

# user = session.query(DiscordUser).get(1)
# print(user.name)
#
# user.name = "hello there"
# print(user.name)
# user.timesDucked += 1
#
# session.commit()

# users = session.query(DiscordUser).all()
# for user in users:
#     print(user.name)

# session.close()


# Contains the classes and functions used to log the duck counts to a file, like a database
import duckLogger

# Adds environment variables
# Will remove load_dotenv() if I host it on Heroku

# load_dotenv()
TOKEN = os.getenv('DUCK_TOKEN')
# DATABASE = os.getenv("DATABASE_URL")

# Monke token, used for testing.
# TOKEN = os.getenv('TEST_TOKEN')
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
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='My amazing King James UwU <3'))

    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    # Reset function
    if message.content == "!reset":
        if message.author.name == "God King James" or message.author.name == "rianjohnsonstan <3 UwU" or message.author.name == "Luv2ski2":
            users = session.query(DiscordUser).all()
            for user in users:
                session.delete(user)
            session.commit()
            await message.channel.send("Duck counts deleted!")

    if message.content == "!ducks":
        # Can't be called from the devotion channel
        if message.channel.name == "temple":
            return
        send = ""
        users = session.query(DiscordUser).all()
        # users = duckLogger.getInfo()
        for user in users:
            send = send + f'{user.name} has devoted {user.timesDucked} times\n'
        await message.channel.send(send)

    if message.content == "H":
        await message.channel.send("It's working")

    if message.channel.name == "temple":
        # If bot sends message, doesn't count
        if message.author == client.user:
            return

        # users = duckLogger.getInfo()
        users = session.query(DiscordUser).all()
        # for user in users:
        #     print(user.formatReturn())
        # userID = duckLogger.inUserList(message.author.name, users)

        userID = inDatabase(message.author.name, users)
        print(userID)

        if userID == "no user with that name":
            print("|||||||")
            newUser = DiscordUser(name=message.author.name)
            session.add(newUser)
            session.commit()


            # user = duckLogger.User(message.author.name, 1)
            # users.append(user)
        else:
            print("-------")
            user = session.query(DiscordUser).get(userID)
            user.timesDucked += 1
            session.commit()

            # users[userID].timesDucked = int(users[userID].timesDucked) + 1
            # print(users[userID].timesDucked)
        # duckLogger.writeInfo(users)
        print('hi')
    else:
        print('hello')

    print(message.content)
    session.close()


client.run(TOKEN)