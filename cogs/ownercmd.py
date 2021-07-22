import random
import string
import discord
from discord.ext import commands
import json
from discord.utils import get

# This contains all the commands serer admins can use. 
class Admin_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # Error handler
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            errorEmbed = discord.Embed(
                title="Error!",
                description="Make sure you put all required values.\n\nError was: `{}`".format(
                    str(error).capitalize()
                ),
                color=0xC4002B,
            )
            errorEmbed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            await ctx.channel.send(embed=errorEmbed)
        else:
            pass
    # Sever admins can get a list of all the active and none active licenses in that specific server only. 
    @commands.command()
    @commands.has_permissions(administrator=True, manage_roles=True)
    async def licenses(self, message):
        server = str(message.guild.id)
        user_id = message.author.id
        userss = open("./data_storage/user_data.json")
        userss = open("./data_storage/sub.json")
        server123 = json.load(userss)
        x = server123.get("Subscriptions").get(server)
        non_ac = []
        for y in x:
            timel = "|seconds " + str(x[y]["Sub_length"])
            Role = '| Role assigned "' + str(x[y]["Role"]) + '"'
            TotaL_len = y + timel + Role
            non_ac.append(TotaL_len)
        s = "\n"
        s = s.join(non_ac)
        with open("./temp/none_active_codes.txt", "w") as c:
            c.write(str(s))
        member = await message.guild.fetch_member(user_id)
        await member.send(file=discord.File("./temp/none_active_codes.txt"))
        userss = open("./data_storage/user_data.json")
        server123 = json.load(userss)
        y = server123.get("USER_DATA").get(server)
        all_ac = []
        for x in y:
            user_give = y[x]["ID"]
            expiration = y[x]["Expiration"]
            user_give = str(user_give)
            expiration = str(expiration)
            total = f'User ID: "{user_give}" | Expiration in UNIX "{expiration}" '
            all_ac.append(total)
        s = "\n"
        s = s.join(all_ac)
        with open("./temp/active_codes.txt", "w") as c:
            c.write(str(s))
        await member.send(file=discord.File("./temp/active_codes.txt"))
        # To empty out codes after sending it over.
        with open("./temp/active_codes.txt", "w") as c:
            c.write("Removed")
        with open("./temp/none_active_codes.txt", "w") as c:
            c.write("Removed")
    
    # If multiple servers using the same bot prefix can be changable.
    @commands.command()
    @commands.has_permissions(administrator=True, manage_roles=True)
    async def prefix(self, message, new_prefix):
        arg1 = new_prefix
        arg1 = str(arg1)
        openf = open("prefixes.json")
        data_load = json.load(openf)
        if data_load.get(str(message.guild.id)) == "None":
            data_load[str(message.guild.id)] = ""
        data_load[str(message.guild.id)] = arg1
        json.dump(data_load, open("prefixes.json", "w"), sort_keys=True, indent=2)
        openf.close()
        await message.channel.send(f"Prefix changed to {arg1}")
    
    # Remove command
    @commands.command(description="There are two removeable elements. \n1.user\n2.unused\n\nTo remove/cancel a user subscription you can use the command below. The role that was assigned to the user given with the subscription key will only be removed.\nExample below:\n\n!remove user @someone # If you don't want to mention someone you can replace @someone with the user id.\n\nTo remove all unused licenses use the command:\n!remove unused.")
    @commands.has_permissions(administrator=True, manage_roles=True)
    async def remove(self, message, removeable_element, member: discord.Member = None):
        server = str(message.guild.id)
        if str(removeable_element) == "unused":
            user_inf = open("./data_storage/sub.json")
            data_load = json.load(user_inf)
            data_load["Subscriptions"][server] = {}
            json.dump(data_load, open("./data_storage/sub.json", "w"), sort_keys=True, indent=2)
            embedVar = discord.Embed(
                title="Success!", description="**Task Completed**", color=0x34EB7D
            )
            await message.channel.send(embed=embedVar)
        elif str(removeable_element) == "user" and (member) != None:
            user_inf = open("./data_storage/user_data.json")
            data_load = json.load(user_inf)
            id_num = str(member.id)
            guild = self.bot.get_guild(int(server))
            role = data_load["USER_DATA"][server][id_num]["Role"]
            role = get(guild.roles, name=role)
            await member.remove_roles(role)
            del data_load["USER_DATA"][server][id_num]
            json.dump(data_load, open("./data_storage/user_data.json", "w"), sort_keys=True, indent=2)
            embedVar = discord.Embed(
                title="Success!", description="**Task Completed**", color=0x34EB7D
            )
            embedVar.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            await message.channel.send(embed=embedVar)
        else:
            embedVar = discord.Embed(
                title="Error!",
                description="**Something is not quite right.**",
                color=0xDB0909,
            )
            embedVar.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            await message.channel.send(embed=embedVar)
    # To generate random subscriptions.
    @commands.command(description='A list of time methods you can use for expiration.\n\n1. (m): Use if setting expiration with minutes.\n2. (h): Use if setting expiration with hours.\n3. (d): Use if setting expiration with days.\n4. (w): Use if setting expriation with weeks.\n5. (n): Use if setting expiration with months.\n\nExamples **Note**: Prefix will varie:\n!gen 1 1n @testRole #This command will generate 1 subscription of the role @testRole for 1 month.\n\n!gen 4 30m 123456 # This will generate 4 subscription keys for the role given the ID. Note it does not matter if you mention the role or give the role ID both will work.')
    @commands.has_permissions(administrator=True, manage_roles=True)
    async def gen(self, message, how_many_subs, expiration_time, role: discord.Role):
        try:
            arg = expiration_time
            arg1 = how_many_subs
            times = int(arg1)
            if times > 20:
    
                embedVar = discord.Embed(
                title="Error!", description="You can only generate 20 or less at a time", color=0xab031a)
                embedVar.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                await message.channel.send(embed=embedVar)
                return
            role = str(role)
            server = str(message.guild.id)
            channel = message.channel
            member = await message.guild.fetch_member(message.author.id)
            user_inf = open("./data_storage/sub.json")
            data_load = json.load(user_inf)
            if data_load.get("Subscriptions").get(server) == None:
                data_load["Subscriptions"][server] = {}
                json.dump(data_load, open("./data_storage/sub.json", "w"), sort_keys=True, indent=2)
            userstf = open("./data_storage/user_data.json")
            use_d = json.load(userstf)
            if use_d.get("USER_DATA").get(server) == None:
                use_d["USER_DATA"][server] = {}
                json.dump(use_d, open("./data_storage/user_data.json", "w"), sort_keys=True, indent=2)
            value = arg[-1].lower()
            if str(value) == "m":
                seconds = int(arg[:-1]) * 60
            if str(value) == "h":
                seconds = int(arg[:-1]) * 3600
            if str(value) == "d":
                seconds = int(arg[:-1]) * 86400
            if str(value) == "w":
                seconds = int(arg[:-1]) * 604800
            if str(value) == "n":
                seconds = int(arg[:-1]) * 2592000
            total = []
            for x in range(times):
                code = "".join(
                    random.choices(
                        string.ascii_uppercase + string.digits + string.ascii_lowercase,
                        k=16,
                    )
                )
                data_load["Subscriptions"][server][code] = {
                    "Sub_length": seconds,
                    "Role": role,
                }
                json.dump(data_load, open("./data_storage/sub.json", "w"), sort_keys=True, indent=2)
                total.append(
                    "**"
                    + code
                    + "** : Role - **"
                    + str(data_load["Subscriptions"][server][code]["Role"])
                    + "** |Length Seconds - "
                    + str(data_load["Subscriptions"][server][code]["Sub_length"])
                )
            new = "\n".join(total)
            embedVar = discord.Embed(
                title="Codes below.", description=new, color=0x34EB7D
            )
            embedVar.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            await member.send(embed=embedVar)
            Success = discord.Embed(
                title="Success!",
                description="Check your DMS for the subscription details!",
                color=0x34EB7D,
            )
            Success.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            await channel.send(embed=Success)
            user_inf.close()

        except Exception as e:
            print(e)


def setup(bot):
    bot.add_cog(Admin_Commands(bot))
