# 数据文件结构

## 用户数据

```txt
UserData
+---[name].emp
+---data
    +---songs
    |   +---[filename]-[sid].[type]
    |   +---...
    +---videos
    |   +---[filename]-[sid].[type]
    |   +---...
    +---lyrics
    |   +---[filename]-[sid].lyc
    |   +---...
    +---covers
        +---[filename]-[sid].[type]
        +---...
```

- `[name].emp`：用户数据文件
    ```json
    {
        "songs":[
            {
                "filename":"XXX",
                "title":"XXX",
                "sid":"XXXXX",
                "metadata":{
                    "artists":["a1","..."],
                    "source":"bilibili",
                    "download":{},
                    "length":60000.0
                },
                "song-type":"mp3",
                "cover-type":"jpg",
                "has-lyric":true,
                "show-lyric":false,
                "has-vedio":true,
                "vedio-sound":true,
                "vedio-type":"mp4",
                "show-vedio":true
            }
        ],
        "songlists":[
            {
                "title":"XXX",
                "slid":"XXXXX",
                "songs":[
                    "sid1",
                    "sid2",
                    "..."
                ]
            }
        ],
        "session":{
            "last-songlist":"slid",
            "last-song":"sid",
            "play-mode":"ord"
        }
    }
    ```