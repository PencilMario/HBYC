######################################
#***************HBYC Bot*************#
#*********Author:dragonyc1002********#
#*******Release Date:2022.07.05******#
#************Version:0.0.5***********#
#********License: BSD 3-Clause*******#
#****Develop OS: Ubuntu 20.04 LTS****#
######################################
channel_id = 995187515013202082
notice_ban_id = 995576399148634162

import discord
from discord.ext import commands, bridge
from discord.commands import slash_command, Option

import json, os, time

#from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = bridge.Bot(command_prefix="c!", intents=intents)
client.remove_command(name="help")

@client.event
async def on_ready():
    print("Bot Logined")
    print(client.user)
    print(f"Logined at", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print("------------------------")
    
    for guild in client.guilds:
        print(guild.id, guild.name)
    print("------------------------")

    await client.change_presence(activity=discord.Game('c!help'))

@client.event
async def on_member_join(member):
    print("Recognised that a member called " + member.name + " joined")
    embed=discord.Embed(title=f":tada:欢迎 {member.name}", description=f"感谢加入 MAS-CN讨论组!\n在开始聊天之前，请确保您已经阅读 **#守则-rules**") # F-Strings!
    try:
        embed.set_thumbnail(url=member.avatar.url)
    except:
        pass
    channel = client.get_channel(channel_id)
    welcomechannel = await client.fetch_channel(channel_id)
    await welcomechannel.send(embed=embed)

@client.event
async def on_member_ban(guilds, member):
    print("Recognised that a member called " + member.name + " banned")
    embed=discord.Embed(title=f":tada:喜讯之 **{member.name}**", description=f"被在线的Admin永久封禁，好死喵~") # F-Strings!
    try:
        embed.set_thumbnail(url=member.avatar.url)
    except:
        pass
    ban_channel = client.get_channel(notice_ban_id)
    notice_ban_channel = await client.fetch_channel(notice_ban_id)
    await notice_ban_channel.send(embed=embed)    

@client.bridge_command(name = "load", description = "Load the Cog_Extension")
async def load(
    ctx,
    extension: Option(str, "Enter Extension Name", choices=["chat", "event","music", "help", "user"]),
    password: Option(str, "passwd")
):
    PermessionDeniedFrom = (f"{ctx.author} at {ctx.author.guild.name}")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    if password == passwd :
        client.load_extension(f"cmds.{extension}")
        await ctx.respond(f"加載Cog: {extension} 完成!")
        print(f"Loaded {extension}")
        print("at", timestamp)

    else:
        await ctx.respond("密碼錯誤，如錯誤超過3次將直接把你列入使用黑名單(ban)，未來將無法使用HBYC")
        print("###Someone tried to load the cog###", PermessionDeniedFrom)


@client.bridge_command(name = "unload", description = "Un-Load the Cog_Extension")
async def unload(
    ctx,
    extension: Option(str, "Enter Extension Name", choices=["chat", "event","music", "help", "user"]),
    password: Option(str, "passwd")
):
    PermessionDeniedFrom = (f"{ctx.author} at {ctx.author.guild.name}")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    if password == passwd :
        client.unload_extension(f"cmds.{extension}")
        await ctx.respond(f"關閉Cog: {extension} 完成!")
        print(f"UnLoaded {extension}")
        print("at", timestamp)

    else:
        await ctx.respond("密碼錯誤，如錯誤超過3次將直接把你列入使用黑名單(ban)，未來將無法使用HBYC")
        print("###Someone tried to unload the cog###", PermessionDeniedFrom)


@client.bridge_command(name = "reload", description = "Re-Load the Cog_Extension")
async def reload(
    ctx,
    extension: Option(str, "Enter Extension Name", choices=["chat", "event","music", "help", "user"]),
    password: Option(str, "passwd")
):
    PermessionDeniedFrom = (f"{ctx.author} at {ctx.author.guild.name}")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    if password == passwd :
        client.reload_extension(f"cmds.{extension}")
        await ctx.respond(f"重新加載Cog: {extension} 完成!")
        print(f"ReLoaded {extension}")
        print("at", timestamp)

    else:
        await ctx.respond("密碼錯誤，如錯誤超過3次將直接把你列入使用黑名單(ban)，未來將無法使用HBYC")
        print("###Someone tried to reload the cog###", PermessionDeniedFrom)


@client.bridge_command(name="custom", description="owner only")
async def custom(ctx, presence: Option(str, "presence name"), password: Option(str, "passwd")):
    PermessionDeniedFrom = (f"{ctx.author} at {ctx.author.guild.name}")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    if password == passwd :
        await client.change_presence(activity=discord.Game(name=presence))
        await ctx.respond(f"changed presence to {presence} done.")
        print("/custom")
        print(f"Presence changed:{presence}")
        print("from", ctx.author.guild.name)
        print("by:", ctx.author)
        print(f"at {timestamp}")
        print("-------")
    
    else:
        await ctx.respond("密碼錯誤，如錯誤超過3次將直接把你列入使用黑名單(ban)，未來將無法使用HBYC")
        print("### Someone tried to use custom presence as non-owner failed ###", PermessionDeniedFrom)
        print("User:", ctx.author)
        print(f"at {timestamp}")
        print("-------")


with open("config.json", mode="r", encoding="utf8") as config:
    conf = json.load(config)


for filename in os.listdir("./cmds"):
    if filename.endswith(".py"):
        client.load_extension(f"cmds.{filename[:-3]}")


#load_dotenv()
#token = os.getenv("DISCORD_TOKEN")
passwd = os.getenv("password")


if __name__ == "__main__":
    client.run(conf["token"])    
