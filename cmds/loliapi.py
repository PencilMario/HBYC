######################################
#********HBYC Bot Help Commands******#
#*********Author:dragonyc1002********#
#*******Release Date:2022.07.05******#
#************Version:0.0.5***********#
#********License: BSD 3-Clause*******#
#****Develop OS: Ubuntu 20.04 LTS****#
######################################
LOLIAPI = "https://api.lolicon.app/setu/v2"

import discord
from discord.ext import bridge
from discord.ext.bridge.core import BridgeOption
from core.classes import Cog_Extension

import time, requests


class Loliapi(Cog_Extension):
    @bridge.bridge_command(name="setu", description="来张色图")
    async def setu(self, ctx):
        urldata = requests.get(LOLIAPI)
        json = urldata.json()
        await ctx.respond(json["data"][0]["urls"]["original"])

    @bridge.bridge_command(name="setutag", description="来张带指定Tag的色图")
    async def help(self, ctx, tag: BridgeOption(str, "色图tag", required=False) = None):
        try:
            urldata = requests.get("https://api.lolicon.app/setu/v2?tag="+tag)
            json = urldata.json()
            await ctx.respond(json["data"][0]["urls"]["original"])
        except:
            await ctx.respond("色图tag获取失败了...")

def setup(client):
    client.add_cog(Loliapi(client))