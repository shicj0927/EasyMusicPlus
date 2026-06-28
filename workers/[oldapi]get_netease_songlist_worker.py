import json
from websocket import create_connection
import requests


def get_current_playlist_by_ws(cdp_ws_url: str):
    js = r"""
(() => {
    const rootDom = document.getElementById("root");
    const key = Object.keys(rootDom).find(k => k.startsWith("__reactContainer"));
    if (!key) return null;
    const root = rootDom[key];
    function dfs(f) {
	    if (!f) return null;
    	const p = f.memoizedProps;
    	if (
        	p &&
        	p.playlist &&
        	p.dispatch &&
        	typeof p.id === "string"
    	) {
        	return f;
    	}
    	return (
        	dfs(f.child) ||
        	dfs(f.sibling)
    	);
	}
    return dfs(root).memoizedProps.playlist;
})()
"""

    ws = create_connection(cdp_ws_url)

    try:
        ws.send(json.dumps({
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {
                "expression": js,
                "returnByValue": True
            }
        }))
        while True:
            resp = json.loads(ws.recv())
            if resp.get("id") != 1:
                continue
            if "error" in resp:
                raise RuntimeError(resp["error"])
            result = resp["result"]["result"]
            if result.get("type") == "object":
                return result.get("value")
            return result.get("value")
    finally:
        ws.close()

def get_current_playlist_by_url(url: str):
    print(url)
    targets = requests.get(f"{url.rstrip('/')}/json", timeout=5).json()
    ws_url = None
    for target in targets:
        if (
            target.get("type") == "page"
            and target.get("title") == "网易云音乐"
        ):
            ws_url = target["webSocketDebuggerUrl"]
            break
    if ws_url is None:
        raise RuntimeError("未找到网易云音乐页面")
    print(ws_url)
    return get_current_playlist_by_ws(ws_url)

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
import traceback

class getNeteaseSonglistWorker(QObject):
    getNeteaseSonglistFinishedSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
    
    @pyqtSlot(str)
    def get(self, url):
        try:
            self.getNeteaseSonglistFinishedSignal.emit(get_current_playlist_by_url(url))
        except Exception as e:
            traceback.print_exc()