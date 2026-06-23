html="""
<!DOCTYPE html>
<html lang="zh-CN">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title id="pagetitle"></title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box
        }

        body {
            background: #f5f7fb;
            font-family: "Segoe UI", sans-serif;
            color: #222;
            padding: 32px
        }

        .container {
            max-width: 980px;
            margin: auto
        }

        .header {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 28px
        }

        .title {
            font-size: 34px;
            font-weight: 700
        }

        .copy-btn {
            border: none;
            background: #e8eefc;
            color: #356dff;
            padding: 8px 14px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 14px
        }

        .list {
            display: flex;
            flex-direction: column;
            gap: 14px
        }

        .item {
            display: flex;
            align-items: center;
            gap: 18px;
            background: #fff;
            border-radius: 18px;
            padding: 16px;
            box-shadow: 0 4px 14px rgba(0, 0, 0, .06)
        }

        .cover {
            width: 72px;
            height: 72px;
            border-radius: 14px;
            object-fit: cover;
            flex-shrink: 0
        }

        .info {
            flex: 1;
            min-width: 0
        }

        .song-title {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 6px
        }

        .artist {
            color: #666;
            font-size: 14px
        }

        .links {
            display: flex;
            gap: 10px;
            flex-wrap: wrap
        }

        .link-btn {
            text-decoration: none;
            padding: 10px 16px;
            border-radius: 12px;
            background: #edf2ff;
            color: #356dff;
            font-size: 14px;
            font-weight: 600
        }

        .footer {
            text-align: center;
            margin-top: 28px;
            color: #888;
            font-size: 14px
        }

        @media(max-width:700px) {
            body {
                padding: 16px
            }

            .item {
                align-items: flex-start;
                flex-wrap: wrap
            }

            .links {
                margin-top: 12px
            }
        }
    </style>
</head>

<body>
    <div class="container">
        <div class="header">
            <div class="title" id="title"></div>
            <div class="number">共 <a id="number"></a> 首歌曲</div>
            <button class="copy-btn" id="copy">复制歌单</button>
        </div>
        <div class="list" id="list">
        </div>
        <div class="footer">
            由 <a href="https://github.com/shicj0927/EasyMusicPlus" target="_blank" style="color: #356dff; text-decoration: underline;">EasyMusicPlus</a> 生成
        </div>
    </div>
    <script>
        function toast(text, time = 2000) {
            let el = document.getElementById("_toast");

            if (!el) {
                el = document.createElement("div");
                el.id = "_toast";

                el.style.cssText = `
		position:fixed;
		left:50%;
		bottom:32px;
		transform:translateX(-50%) translateY(20px);
		background:#222;
		color:#fff;
		padding:12px 18px;
		border-radius:12px;
		font-size:14px;
		opacity:0;
		transition:.25s;
		pointer-events:none;
		z-index:9999;
		`;

                document.body.appendChild(el);
            }

            el.textContent = text;
            el.style.opacity = "1";
            el.style.transform = "translateX(-50%) translateY(0)";

            clearTimeout(el._timer);

            el._timer = setTimeout(() => {
                el.style.opacity = "0";
                el.style.transform = "translateX(-50%) translateY(20px)";
            }, time);
        }
    </script>
    <script>
        data = __DATA__
    </script>
    <script>
        document.getElementById("copy").addEventListener("click", () => {
            const text = data.list
                .map(i => `${i.name} ${i.artist}`)
                .join("\\n");

            navigator.clipboard.writeText(text)
                .then(() => {
                    toast("文本已复制到剪贴板！");
                })
                .catch(() => {
                    toast("复制失败，已在新标签页打开");

                    const html = `
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>复制文本</title>
<style>
body{
	font-family:sans-serif;
	padding:24px;
	line-height:1.7;
	white-space:pre-wrap;
	word-break:break-all;
	background:#f5f7fb;
	color:#222
}
</style>
</head>
<body>${text
                            .replace(/&/g, "&amp;")
                            .replace(/</g, "&lt;")
                            .replace(/>/g, "&gt;")}
</body>
</html>`;

                    const win = window.open("about:blank");

                    if (win) {
                        win.document.open();
                        win.document.write(html);
                        win.document.close();
                    } else {
                        toast("浏览器阻止了弹窗");
                    }
                });
        });
        document.getElementById("pagetitle").textContent = data.title;
        document.getElementById("title").textContent = data.title;
        document.getElementById("number").textContent = data.list.length;
        const listContainer = document.getElementById("list");
        data.list.forEach(item => {
            const itemElement = document.createElement("div");
            itemElement.className = "item";
            itemElement.innerHTML = `
			<div class="info">
				<div class="song-title">${item.name}</div>
				<div class="artist">${item.artist}</div>
			</div>
			<div class="links">
				<a class="link-btn" href="${item.link.url}" target="_blank">${item.link.name}</a>
			</div>
		`;
            listContainer.appendChild(itemElement);
        });
    </script>

</body>

</html>
"""

def get_share_html(json_data):
    tmp=html.replace("__DATA__", json_data)
    return tmp