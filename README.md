# Easy Music Plus

Easy Music Plus 是一个基于 `PyQt6` 的桌面音乐管理与下载工具。项目支持网易云音乐和 Bilibili 音乐/视频下载，并提供本地媒体库、歌单管理、歌词下载、歌单分享等功能。

## 主要功能

- 本地媒体库管理：创建/打开媒体库，保存歌曲与歌单数据
- 歌单管理：增删歌单，拖拽排序歌单和歌曲
- 音乐播放：支持本地播放、暂停、上一首、下一首、播放模式切换
- 下载功能：通过网易云 ID、网易云 URL、Bilibili BV 号或 URL 下载音乐
- 在线搜索：支持网易云和 Bilibili 搜索并快速下载
- 歌词自动获取：网易云音乐歌词下载并保存为 `.lrc`
- 歌单导入：通过网易云歌单 ID 自动获取歌单并批量下载
- 歌单分享：导出歌单为 HTML 格式，方便分享
- 主题切换：支持深色模式与浅色模式
- 会话保存：自动保存上次打开的库、当前歌单、音量、主题等

## 技术栈

- Python 3
- PyQt6
- pycryptodome
- python-mpv
- qtawesome
- requests
- yt_dlp
- pyqtdarkmode

## 安装与运行

1. 克隆或下载项目代码

```bash
git clone <仓库地址>
cd EasyMusicPlus
```

2. 建议创建虚拟环境并激活

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. 安装依赖

```bash
pip install -r requirements.txt
sudo apt install mpv
sudo apt install ffmpeg
```

4. 运行程序

```bash
python main.py
```

> 如果你修改了 `ui/*.ui` 文件，需要重新生成对应的 Python UI 文件（也可以直接使用vscode task构建）：

```bash
find ui -name '*.ui' | while read f; do pyuic6 "$f" -o "$(dirname "$f")/ui_$(basename "${f%.ui}").py"; done
```

## 快速使用

- 启动后通过“新建媒体库”或“打开媒体库”创建/加载本地库
- 在歌单列表中选择歌单，点击“添加歌曲”进行下载或从已有歌曲库中导入
- 通过“下载管理器”输入网易云/Bilibili URL、ID 或关键字搜索并下载
- 在歌单中双击歌曲即可播放，使用进度条控制播放位置
- 可以将歌单导出为 HTML 进行分享

## 文件说明

- `main.py`：应用入口
- `app/`：GUI 界面和对话框逻辑
- `ui/`：PyQt6 UI 文件与生成的 UI Python 文件
- `managers/`：业务逻辑管理代码
- `repositories/`：本地库数据读写与持久化
- `models/`：数据模型定义
- `workers/`：后台搜索与下载线程
- `api/netease.py`：网易云 API 请求封装
- `config.py`：默认 API 配置（弃用）
- `requirements.txt`：Python 依赖列表

## 注意事项

- 项目依赖 `yt_dlp` 下载 Bilibili 视频音频
- 网易云音乐下载依赖网易云 API 的解析与歌词接口
- Windows 下如果需要打包成桌面应用，可参考当前仓库中的 `installer.iss`

## 版权与许可

请参考仓库中的 `LICENSE` 和 `THIRD_PARTY_LICENSES.md` 文件。