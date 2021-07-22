from discord.ext import commands
import os
import json
from discord.ext import tasks
import time
from discord.utils import get

default_prefix = "!"

# This is for custom prefix. 
async def prefix(bot, message):
    with open("prefixes.json") as f:
        prefixes = json.load(f)
    id_1 = message.guild.id
    if bot.user in (message.mentions):
        await message.channel.send(
            f"The prefix is {prefixes.get(str(id_1))} or type {prefixes.get(str(id_1))}help"
        )
    return prefixes.get(str(id_1), default_prefix)


bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    process_queue.start()
    print("PING STARTED")


@tasks.loop(seconds=180)
async def process_queue():
    f = open(
        "./public/user_data.json",
    )
    data = json.load(f)
    try:
        for x in data["USER_DATA"]:
            try:
                for y in data["USER_DATA"][x]:
                    try:
                        for z in data["USER_DATA"][x][y]:
                            expiration = data["USER_DATA"][x][y]["Expiration"]
                            guild = int(data["USER_DATA"][x][y]["Server"])
                            user_id = int(data["USER_DATA"][x][y]["ID"])
                            role = data["USER_DATA"][x][y]["Role"]
                            now = time.time()

                            if expiration - now < 0:
                                guild = bot.get_guild(guild)
                                member = await guild.fetch_member(user_id)
                                role = get(guild.roles, name=role)
                                await member.remove_roles(role)
                                del data["USER_DATA"][x][y]
                                json.dump(
                                    data,
                                    open("./data_storage/user_data.json", "w"),
                                    sort_keys=True,
                                    indent=2,
                                )
                    except:
                        pass
            except:
                pass
    except:
        pass
    f.close()


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
bot.run("ODMzNTI2MzcyMDA1NDQ1NzAy.YHzn7Q.JOVuuDTTRvZEJOu39DkMhMB6Ds0")
# Insert your bot token here
