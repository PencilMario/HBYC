import os
import shutil #对os库的补充
import stat #os 状态
import requests #requests请求第三方库
import json


# def get_music_info(music_id: str):
#     searchResult = requests.get('')
API = "https://netease-cloud-music-api-murex-gamma.vercel.app/"
# url = 'http://music.163.com/weapi/search/suggest/web?csrf_token='

#下载音乐文件到tmp文件夹
def download_music(music_id):
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
    _music_download = requests.get(file_url, stream=True)
    fileName = 'tmp/'+ str(music_id)+'.mp3'
    # 如果 tmp 文件夹未被创建，则创建 tmp 文件夹
    if os.path.exists("tmp/") is not True:
        os.mkdir("tmp/")
    with open(fileName, 'wb') as music:
        music.write(requests.get(_music_download))
    return str(fileName)

# 检测下载可用性
def check_downloadable(id):
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
def get_musicdetail(uid):
    id = str(id)
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
        info["alia"] = None
    info["album"] = res["songs"][0]["al"]["name"]
    info["picurl"] = res["songs"][0]["al"]["picUrl"]
    return info

#清理缓存
def clean_cache():
    if os.path.exists('tmp'):
        for fileList in os.walk('tmp'):
            for name in fileList[2]:
                os.chmod(os.path.join(fileList[0], name), stat.S_IWRITE)
                os.remove(os.path.join(fileList[0], name))
            shutil.rmtree('tmp')
        print("缓存清理完毕")

#队列类
class Queue:
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