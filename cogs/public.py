import discord
import math
from discord.ext import commands
import json
import time
from discord.utils import get

def json_check(check, id_num, server):
    f = open("./data_storage/sub.json")
    data = json.load(f)
    userss = open("./data_storage/user_data.json")
    server123 = json.load(userss)
    if server123.get("USER_DATA").get(server) == None:
        server123["USER_DATA"][server] = {}
        json.dump(server123, open("./data_storage/user_data.json", "w"), sort_keys=True, indent=2)
    # Checks if the servers exist
    # if server123.get('USER_DATA').get(server) == None:
    #   server123['USER_DATA'][server] = {}
    #   json.dump(server123, open('./data_storage/user_data.json','w'), sort_keys=True, indent=2)
    # if data.get('invalid').get(server) == None:
    #   data['invalid'][server] = {}
    #   json.dump(data, open('./data_storage/sub.json','w'), sort_keys=True, indent=2)
    x = data.get("Subscriptions").get(server)
    try:
        leng = x.get(check).get("Sub_length")
        rolen = x.get(check).get("Role")
    except:
        return False
    # Checks subscription if it exists an if so it retruns.
    if not (leng is None):
        del data["Subscriptions"][server][check]
        json.dump(data, open("./data_storage/sub.json", "w"), sort_keys=True, indent=2)
        unixTime = int(time.time())
        expiration = unixTime + (leng)
        f.close()
        userss.close()
        return {
            "Server": server,
            "ID": id_num,
            "Start": unixTime,
            "Expiration": expiration,
            "Role": rolen,
        }
    else:
        return False


def store_info(user_data):

    Add_data = user_data["Server"]
    sub_data = user_data["ID"]
    user_inf = open("./data_storage/user_data.json")
    data_load = json.load(user_inf)
    sub_data = str(sub_data)
    if str(sub_data) in str(data_load):
        del data_load["USER_DATA"][Add_data][sub_data]
        data_load["USER_DATA"][Add_data][sub_data] = user_data
    else:
        data_load["USER_DATA"][Add_data][sub_data] = user_data
    json.dump(data_load, open("./data_storage/user_data.json", "w"), sort_keys=True, indent=2)
    user_inf.close()
    return data_load


class Public_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, message):
        channel = message.channel
        await channel.send("pong")

    @commands.command()
    async def redeem(self, message, subscription):
        arg = subscription
        check = str(arg)
        server = str(message.guild.id)
        channel = message.channel
        id_num = message.author.id
        user_data = json_check(check, id_num, server)
        if user_data != False:
            store_info(user_data)
        else:
            print("We can not go ahead.")
        f = open(
            "./data_storage/user_data.json",
        )
        data = json.load(f)
        role = data["USER_DATA"][str(server)][str(id_num)]["Role"]
        member = message.author
        role = get(member.guild.roles, name=role)
        await member.add_roles(role)
        embedVar = discord.Embed(
            title="Success!",
            description="Subscription added successfully!\n\n**Note**: Once subscription is over role will get removed in a 3 minute interval.",
            color=0x00BD5B,
        )
        embedVar.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        await channel.send(embed=embedVar)

    @commands.command()
    async def expiration(self, message):
        def GetTime(sec):
            try:
                sec = float(sec)
                sec = math.trunc(sec)
                secs = int(sec)
                days = secs // 86400
                hours = (secs - days * 86400) // 3600
                minutes = (secs - days * 86400 - hours * 3600) // 60
                seconds = secs - days * 86400 - hours * 3600 - minutes * 60
                result = (
                    (
                        "{0} day{1}, ".format(days, "s" if days != 1 else "")
                        if days
                        else ""
                    )
                    + (
                        "{0} hour{1}, ".format(hours, "s" if hours != 1 else "")
                        if hours
                        else ""
                    )
                    + (
                        "{0} minute{1}, ".format(minutes, "s" if minutes != 1 else "")
                        if minutes
                        else ""
                    )
                    + (
                        "{0} second{1} ".format(seconds, "s" if seconds != 1 else "")
                        if seconds
                        else ""
                    )
                )
                return result
            except:
                return False

        server = str(message.guild.id)
        channel = message.channel
        id_num = str(message.author.id)
        userss = open("./data_storage/user_data.json")
        server123 = json.load(userss)
        x = server123.get("USER_DATA").get(server).get(id_num)
        try:
            x = x["Expiration"]
            data = time.strftime("%D %H:%M", time.localtime(int(x)))
            elapsed_time = x - time.time()
            x = GetTime(elapsed_time)
            if "-" not in str(x):
                embedVar = discord.Embed(
                    title="",
                    description="Time remaining of your subscription: `" + str(x) + "`",
                    color=0x00BD5B,
                )
                embedVar.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                await channel.send(embed=embedVar)
            else:
                f = open(
                    "./data_storage/user_data.json",
                )
                data = json.load(f)
                embedVar = discord.Embed(
                    title="Bad News!",
                    description="Your subscription is over it will be removed shortly",
                    color=0xBD2F00,
                )
                embedVar.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                await channel.send(embed=embedVar)
                guild = self.bot.get_guild(int(server))
                member = await guild.fetch_member(int(id_num))
                role = data["USER_DATA"][server][id_num]["Role"]
                role = get(guild.roles, name=role)
                await member.remove_roles(role)
                del data["USER_DATA"][server][id_num]
                json.dump(data, open("./data_storage/user_data.json", "w"), sort_keys=True, indent=2)
        except:
            embedVar = discord.Embed(
                title="Error!",
                description="No subscription expiration found!",
                color=0xE63629,
            )
            embedVar.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            await channel.send(embed=embedVar)


def setup(bot):
    bot.add_cog(Public_Commands(bot))
