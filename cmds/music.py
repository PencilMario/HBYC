######################################
#********HBYC Bot Music Commands*****#
#*********Author:dragonyc1002********#
#*******Release Date:2022.07.05******#
#************Version:0.0.5***********#
#********License: BSD 3-Clause*******#
#****Develop OS: Ubuntu 20.04 LTS****#
######################################
API = "https://netease-cloud-music-api-murex-gamma.vercel.app/"

import discord
from discord.ext import commands, bridge
from discord.ext.bridge.core import BridgeOption
from core.classes import Cog_Extension
from discord.utils import get
from discord import ApplicationCommand, FFmpegPCMAudio
from youtube_dl import YoutubeDL
import netease_dl

import json, time, requests, urllib3

Queue = netease_dl.Queue()

with open("config.json", mode="r", encoding="utf8") as jfile:
    config = json.load(jfile)


class Music(Cog_Extension):
    @bridge.bridge_command(name="join", description="讓機器人加入你所在的語音頻道", aliases=["j"])
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.respond("請先加入一個語音頻道")

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()
        await ctx.respond(f"已加入`{ctx.author.voice.channel}`")
        print("/join")
        print("from", ctx.author.guild.name)
        print("at", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("by", ctx.author)
        print("------")


    @bridge.bridge_command(name="leave", description="讓機器人離開他所在的語音頻道", aliases=["l"])
    async def leave(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
            await ctx.respond(f"已離開`{ctx.author.voice.channel}`")
            #NM
            if Queue.is_empty() is False:
                Queue.clear()
            netease_dl.clean_cache()
            print("/leave")
            print("from", ctx.author.guild.name)
            print("at", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print("by", ctx.author)
            print("------")

        else:
            await ctx.respond(f"{ctx.author.mention} 我並不在任何語音頻道中")

    @bridge.bridge_command(name="music_search", description="搜一首歌 歌名请用引号包裹")
    async def music_search(self, ctx, songname: BridgeOption(str, "歌曲名称", required=True)="Never Gonna Give You Up"):
        songlist = []
        says = ""
        if songname == None:
            await ctx.respond("请输入歌名 带空格请用引号包裹")
        else:
            song = requests.get(API + "search?keywords=" + songname + "&limit=12")
            songs = song.json()
            result = songs["result"]["songs"]
            songlist.append("id  |  名称 - 歌手")
            for i in result:
                name ="**" + str(i['id']) + "**" + "  |  " + i['name'] + " - " + i['artists'][0]["name"]
                songlist.append(name)
            for i in songlist:
                says = says + i +"\n"
        if says != "":
            embed = discord.Embed()
            if songname == "Never Gonna Give You Up":
                says.append("笨比知道你忘记输入歌名了，所以小小的骗一下也无所谓吧")
            embed.add_field(name=":musical_note: 搜索结果", value=says, inline=False)
            embed.set_footer(text="如果关键词包含空格，请用\"引号\"包裹")
            await ctx.respond(embed)
        else:
            await ctx.respond("未搜索到结果")

    @bridge.bridge_command(name="music_add_queue", description="将音乐id添加至待播放列表")
    async def play(self, ctx, url: BridgeOption(str, "請將連結貼在這裡", required=False) = None):
        pass

    @bridge.bridge_command(name="music_play", description="播放指定音乐id")
    async def play(self, ctx, uid: BridgeOption(str, "音乐的id", required=False) = None):
        if ctx.voice_client is None:
           return await ctx.send("先使用c!join")
        # print(music_kwords)
        if uid == None:
            embed = discord.Embed(title="None Id", description="请输入正确的ID喵", color=0xeee657)
            return await ctx.send(embed=embed)
        music_info = netease_dl.check_downloadable(uid)
        if music_info == False:
            embed = discord.Embed(title="获取播放链接失败", description="可能为黑胶VIP歌曲或者该歌曲无版权", color=0xeee657)
            return await ctx.send(embed=embed)
        #正在播放 又有新的歌曲就添加到队列
        if ctx.voice_client.is_playing():
            Queue.enqueue(uid)
            print("0：", Queue.music_list)
            return
        #没有播放 直接添加到队列
        Queue.enqueue(music_info)
        print("1：",Queue.music_list)

        while True:
            # 等待播放结束
            while ctx.voice_client.is_playing():
                await asyncio.sleep(1)
            print("3：", Queue.music_list)
            if Queue.is_empty() is False:
                music_detail = Queue.dequeue()
                url = music_detail["url"]
                musicId = music_detail["musicId"]
                musicPic = music_detail["musicPic"]
                musicName = music_detail["musicName"]
                musicArtists = music_detail["musicArtists"]
                # global lyric
                # lyric = music_info['lyric']
                #播放
                musicFileName = netease_dl.download_music(uid)
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(musicFileName), volume=0.6)
                info = netease_dl.get_musicdetail(uid)
                embed = discord.Embed(title="正在播放: "+ info['name']) 
                if info['alia'] != None:
                    embed.add_field(name=info['alia']) 
                embed.add_field(name="歌手", value=info['author'], inline=False) 
                embed.add_field(name="专辑", value=info['album']) 
                embed.set_thumbnail(url=info["picurl"])
                ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
                await ctx.send(embed=embed)

            else:
                print("2：", Queue.music_list)
                return




# YM 分割线----------------------------------------------------------------


    @bridge.bridge_command(name="play", description="讓機器人播放音樂，目前只能一次播放一首而且只能使用影片網址，音樂功能會在之後的版本再行改善", aliases=["pl"])
    async def play(self, ctx, url: BridgeOption(str, "請將連結貼在這裡", required=False) = None):
        if url == None:
            await ctx.respond("請填入網址")

        else:
            YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
            FFMPEG_OPTIONS = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            voice = get(self.client.voice_clients, guild=ctx.guild)

            if not voice.is_playing():
                with YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(url, download=False)
                URL = info['url']
                voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                voice.is_playing()
                now_playing = f"現正播放：{url}"
                await ctx.respond(now_playing)
                print("/play", url)
                print("from", ctx.author.guild.name)
                print("at", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                print("by", ctx.author)
                print("------")

            else:
                await ctx.respond(f"{ctx.author.mention}我已經在播音樂了！")
                return
        

    @bridge.bridge_command(name="resume", description="繼續播放原本在播放的音樂")
    async def resume(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if not voice.is_playing():
            voice.resume()
            await ctx.respond("繼續播放音樂")
            print("/resume")
            print("from", ctx.author.guild.name)
            print("at", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print("by", ctx.author)
            print("------")
        
        else:
            await ctx.respond(f"{ctx.author.mention} 我根本沒有在播音樂")
            

    @bridge.bridge_command(name="pause", description="暫停正在播放的音樂")
    async def pause(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.pause()
            await ctx.respond("暫停播放音樂")
            print("/pause")
            print("from", ctx.author.guild.name)
            print("at", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print("by", ctx.author)
            print("------")


    @bridge.bridge_command(name="stop", description="結束目前正在播放的音樂")
    async def stop(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.stop()
            await ctx.respond(f"{ctx.author.mention} 音樂已停止")
            print("/stop")
            print("from", ctx.author.guild.name)
            print("at", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print("by", ctx.author)
            print("------")
        
        else:
            await ctx.respond(f"{ctx.author.mention} 我根本沒有在播音樂")

def setup(client):
    client.add_cog(Music(client))