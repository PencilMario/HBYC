# 一个随便摸鱼的Discord bot

基于[HBYC v0.0.5](https://github.com/dragonyc1002/HBYC)编写

嘛，其实就是在[原功能](README%20copy.md)上加了点别的东西  
指令前缀依然为c!  

## 额外功能

> <>为可选，[]为必填

1. lolicon api  

简单的色图功能  
`setu` - 随机获取一张色图  
`setutag [tag]` - 随机获取一个带指定标签的色图

2. netease music  
网易云音乐点歌功能，API来自[NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi)  

>网易云系列功能前缀一般为music
>需要先用join加入频道

`music_search <name>` - 搜索一首歌曲 ~~不填会被rickroll~~  
`music_play [id]` - 播放指定id的歌曲  
`music_next` - 跳至下一首
`music_queue` - 查看队列
`music_remove [id]` - 删除播放队列中指定id的歌曲
`music_suggest [num] [tag]` - 添加num首标签为tag的歌曲 (使用斜杠指令时可以选择tag)

部分歌曲相关因为HBYC本身自带了YM点歌，所以会冲突，以后再修辣~    