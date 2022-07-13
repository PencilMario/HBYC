######################################
#********HBYC Bot Music Commands*****#
#*********Author:dragonyc1002********#
#*******Release Date:2022.07.05******#
#************Version:0.0.5***********#
#********License: BSD 3-Clause*******#
#****Develop OS: Ubuntu 20.04 LTS****#
######################################
from dis import disco
import random
from winreg import QueryInfoKey
import discord
from discord.ext import commands, bridge
from discord.ext.bridge.core import BridgeOption
from core.classes import Cog_Extension
from discord.utils import get
from discord import ApplicationCommand, Embed, FFmpegPCMAudio
from youtube_dl import YoutubeDL
from urllib import parse

import json, time
import requests
import os, shutil, asyncio

API = "https://netease-cloud-music-api-murex-gamma.vercel.app"

MUSIC_TAGS=['华语', '欧美', '韩语', '日语', '粤语',  'R&B/Soul', '怀旧', '小语种', '学习', '夜晚', '运动', 'ACG', '影视原声', '流行', '摇滚', '古风', '民谣', '乡村', '浪漫', '经典', '世界音乐', '轻音乐', '电子', '器乐', '说唱']

with open("config.json", mode="r", encoding="utf8") as jfile:
    config = json.load(jfile)
class NQueue:
    def __init__(self):
        self.music_list = []

    def is_empty(self):
        return self.music_list == []

    def enqueue(self, music_info):
        self.music_list.insert(0, music_info)

    def dequeue(self):
        return self.music_list.pop()

    def size(self):
        return len(self.music_list)

    def clear(self):
        self.music_list.clear()

Queue = NQueue()
headers={'Connection':'Close',}

class Music(Cog_Extension):
    def download_music(self, music_id):
        id = str(music_id)
        url = API + "/song/url?id=" + id
        music = requests.get(url)
        try:
            getdata = music.json()
        except Exception:
            return False
        file_url = getdata["data"][0]["url"]
        if file_url == None:
            return False
        _music_download = requests.get(file_url)
        fileName = 'tmp/'+ str(music_id)+'.mp3'
        # 如果 tmp 文件夹未被创建，则创建 tmp 文件夹
        if os.path.exists("tmp/") is not True:
            os.mkdir("tmp/")
        with open(fileName, 'wb') as music:
            music.write(_music_download.content)
        return str(fileName)

    def return_url(self, music_id):
        id = str(music_id)
        url = API + "/song/url?id=" + id
        music = requests.get(url)
        try:
            getdata = music.json()
        except Exception:
            return False
        file_url = getdata["data"][0]["url"]
        return file_url

    # 检测下载可用性
    def check_downloadable(self, id):
        id = str(id)
        url = API + "/song/url?id=" + id
        music = requests.get(url)
        try:
            getdata = music.json()
        except Exception:
            return False
        file_url = getdata["data"][0]["url"]
        if file_url == None:
            return False
        else:
            return True

    # 获取歌曲信息
    def get_musicdetail(self, uid):
        id = str(uid)
        url = API + "/song/detail?ids=" + id
        music = requests.get(url)
        res = music.json()
        info = {}
        info["name"] = res["songs"][0]["name"]
        info["id"] = res["songs"][0]["id"]
        info["author"] = res["songs"][0]["ar"][0]["name"]
        try:
            info["alia"] = res["songs"][0]["alia"][0]
        except:
            info["alia"] = ""
        info["album"] = res["songs"][0]["al"]["name"]
        info["picurl"] = res["songs"][0]["al"]["picUrl"]
        return info

    #清理缓存
    def clean_cache(self):
        if os.path.exists('tmp'):    
            shutil.rmtree('tmp')
            print("缓存清理完毕")



    @bridge.bridge_command(name="join", description="讓機器人加入你所在的語音頻道(避免使用斜杠指令！！)")
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.respond("請先加入一個語音頻道")
        if ctx.voice_client is not None:
            await ctx.respond("bot正在一个语音频道")
        await ctx.author.voice.channel.connect()
        await ctx.send(f"已加入`{ctx.author.voice.channel}`")
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
            print("/leave")
            print("from", ctx.author.guild.name)
            print("at", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print("by", ctx.author)
            print("------")
            self.clean_cache()
            Queue.clear()

        else:
            await ctx.respond(f"{ctx.author.mention} 我並不在任何語音頻道中")

    @bridge.bridge_command(name="music_search", description="搜一首歌 歌名请用引号包裹")
    async def music_search(self, ctx, songname: BridgeOption(str, "歌曲名称", required=True)="Never Gonna Give You Up"):
        songlist = []
        says = ""
        if songname == None:
            await ctx.respond("请输入歌名 带空格请用引号包裹")
        else:
            song = requests.get(API + "/search?keywords=" + parse.quote(songname) + "&limit=12")
            songs = song.json()
            result = songs["result"]["songs"]
            songlist.append("id  |  名称 - 歌手\n")
            for i in result:
                name ="**" + str(i['id']) + "**" + "  |  " + i['name'] + " - " + i['artists'][0]["name"]
                songlist.append(name)
            for i in songlist:
                says = says + i +"\n"
        if says != "":
            embed = discord.Embed()
            if songname == "Never Gonna Give You Up":
                says = says + "笨比知道你忘记输入歌名了，所以小小的骗一下也无所谓吧"
            embed.add_field(name=":musical_note: 搜索结果", value=says, inline=False)
            embed.set_footer(text="如果使用c!前缀触发指令，而且关键词包含空格，请用\"引号\"包裹")
            await ctx.send(embed=embed)
        else:
            await ctx.respond("未搜索到结果")   
    
    @bridge.bridge_command(name="music_play", description="播放指定音乐id")
    async def music_play(self, ctx, uid: BridgeOption(str, "音乐的id", required=False) = None):
        if ctx.voice_client is None:
           return await ctx.respond("先使用c!join")
        # print(music_kwords)
        if uid == None:
            embed = discord.Embed(title="None Id", description="请输入正确的ID喵", color=0xeee657)
            return await ctx.respond(embed=embed)
        music_info = self.check_downloadable(uid)
        print("1:Check Downloadable")
        if music_info == False:
            embed = discord.Embed(title="获取播放链接失败", description="可能为黑胶VIP歌曲或者该歌曲无版权", color=0xeee657)
            return await ctx.respond(embed=embed)
        #正在播放 又有新的歌曲就添加到队列
        if ctx.voice_client.is_playing():
            Queue.enqueue(uid)
            await ctx.send("已经添加至播放列表")
            print("0：", Queue.music_list)
            return
        #没有播放 直接添加到队列
        Queue.enqueue(uid)
        await ctx.send("已经添加至播放列表")
        print("1：",Queue.music_list)
        voice = get(self.client.voice_clients, guild=ctx.guild)

        while True:
            # 等待播放结束
            while voice.is_playing():
                await asyncio.sleep(1)
            print("3：", Queue.music_list)
            if Queue.is_empty() is False:
                music_detail = Queue.dequeue()
                if not self.check_downloadable(music_detail):
                    embed = discord.Embed(title=str(music_detail) + "获取播放链接失败", description="可能为黑胶VIP歌曲或者该歌曲无版权", color=0xeee657)

                # global lyric
                # lyric = music_info['lyric']
                #播放
                musicFileName = self.download_music(music_detail)
                print("3:Downloaded")
                #source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(musicFileName), volume=0.6)
                info = self.get_musicdetail(music_detail)
                print("3:Get Detailed: " + info['name'])
                embed = discord.Embed(title="正在播放: "+ info['name'], description=info["alia"]) 
                #if info['alia'] != "":
                #    embed.add_field(name=info['alia'], value="") 
                embed.add_field(name="歌手", value=info['author'], inline=False) 
                embed.add_field(name="专辑", value=info['album']) 
                embed.set_footer(text="歌曲id："+str(info["id"]))
                embed.set_thumbnail(url=info["picurl"])
                voice.play(discord.FFmpegPCMAudio(musicFileName))
                voice.is_playing()
                await ctx.send(embed=embed)

            else:
                print("2：", Queue.music_list)
                embed = discord.Embed(title="提示", description="音乐播放列表里已经没有歌了~") 
                await ctx.send(embed=embed)
                return

    @bridge.bridge_command(name="music_next", description="切换至下一首歌")
    async def music_next(self, ctx):
        ctx.voice_client.stop()
        if Queue.size() == 0:
            return await ctx.send("没了~")
        await ctx.respond("快进到下一首>>")

    @bridge.bridge_command(name="music_queue", description="查看播放队列")
    async def music_queue(self, ctx):
        ctx.respond("查询可能花费较长时间...")
        musicnames=""
        if Queue.music_list==[]:
            return await ctx.respond("播放列表里无歌曲")
        for i in Queue.music_list:
            name=self.get_musicdetail(i)
            musicnames = musicnames + (("**{}** | {} - {}\n").format(name["id"], name["name"], name["author"]))
        embed=discord.Embed()
        embed.add_field(name="播放列表", value=musicnames)
        await ctx.send(embed=embed)

    @bridge.bridge_command(name="music_help", description="获取音乐播放教程")
    async def music_help(self, ctx):
        embed=discord.Embed(title="播放帮助(网易云)")
        embed.add_field(name="使用教程", value="1. 进入一个语音频道，使用c!join让机器人加入\n2. 使用c!music_search 搜索歌名\n3. 使用c!music_play <id>播放", inline=False)
        embed.add_field(name="c!join/c!leave", value="加入/离开所在的语音频道（这个指令不要使用斜杠指令）", inline=False)
        embed.add_field(name="c!music_search <name>", value="搜索一首网易云音乐", inline=False)
        embed.add_field(name="c!music_play [id]", value="播放指定id的音乐/将指定id音乐添加至播放列表", inline=False)
        embed.add_field(name="c!music_next", value="播放下一首", inline=False)
        embed.add_field(name="c!music_queue", value="查看播放队列", inline=False)
        embed.add_field(name="c!music_remove [id]", value="从播放队列中移除指定id的歌曲", inline=False)
        embed.add_field(name="c!music_suggest [数量] [风格]", value="随机添加歌曲", inline=False)
        embed.set_footer(text="`<>`为选填，[]为必填")
        await ctx.respond(embed=embed)

    @bridge.bridge_command(name="music_remove", description="从播放队列中移除指定id的歌曲")
    async def music_remove(self, ctx, uid: BridgeOption(str, "音乐的id", required=False) = None):
        removed=False
        if uid == None:
            return await ctx.respond("请输入ID")
        #根据下标删除 因为显示顺序和实际顺序不一样 需要处理一下
        for i in Queue.music_list:
            if uid==i:
                try:
                    Queue.music_list.remove(i)
                    removed=True
                except ValueError:
                   pass
        if removed:
            text="删除歌曲成功"
        else:
            text="删除失败"
        return await ctx.send(text)

    @bridge.bridge_command(name="music_suggest", description="!!无返回消息!! * 随便搞几首获取歌曲推荐（不是完全随机 XD）")
    async def music_suggest(self,ctx,num: BridgeOption(int, "添加歌曲的数量，为防止滥用，值为1-10", required=True),tag :BridgeOption(str, "歌曲TAG风格", choices = MUSIC_TAGS, required=True)):
        if num > 10:
            num = 10
        if num < 1:
            num = 1
        url=API+"/top/playlist?limit=1&order=hot&cat={}".format(tag)
        topplaylist = (requests.get(url)).json()
        playlistid=API+"/playlist/detail?id={}".format(topplaylist["playlists"][0]["id"])
        songlists=requests.get(playlistid).json()
        songs=[]
        s = songlists["playlist"]["trackIds"]
        for song in s:
            songs.append(str(song["id"]))
            print(song['id'])
        Queue.music_list = Queue.music_list + random.sample(songs, num)
        print(Queue.music_list)
        await ctx.send("添加完成")

    @bridge.bridge_command(name="music_queue_clear", description="清空播放列表")
    async def music_queue_clear(self,ctx):
        Queue.clear()
        await ctx.send("ok")


############################################### ym
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
            self.clean_cache()
        
        else:
            await ctx.respond(f"{ctx.author.mention} 我根本沒有在播音樂")

def setup(client):
    client.add_cog(Music(client))