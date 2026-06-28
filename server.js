import express from "express";
import Meting from "./src/meting.js";

const app = express();

app.get("/api/search", async (req, res) => {
    const m = new Meting("netease");
    const result = await m.search(req.query.name, { limit: 30 });
    res.json(JSON.parse(result));
});

app.get("/api/song", async (req, res) => {
    const m = new Meting("netease");
    const result = await m.song(req.query.id);
    res.json(JSON.parse(result));
});

app.get("/api/url", async (req, res) => {
    const m = new Meting("netease");
    const result = await m.url(req.query.id, 128);
    res.json(JSON.parse(result));
});

app.get("/api/lyric", async (req, res) => {
    const m = new Meting("netease");
    const result = await m.lyric(req.query.id);
    res.json(JSON.parse(result));
});

app.get("/api/playlist", async (req, res) => {
    const m = new Meting("netease");
    const result = await m.playlist(req.query.id);
    res.json(JSON.parse(result));
});

app.listen(3000, () => {
    console.log("Meting API running at http://127.0.0.1:3000");
});
