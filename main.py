from flask import Flask, jsonify, Response, request
import requests, json, os

app = Flask(__name__)

FAV_FILE = "favorites.json"

# Favori dosyası yoksa oluştur
if not os.path.exists(FAV_FILE):
    with open(FAV_FILE, "w") as f:
        json.dump([], f)


def load_favorites():
    with open(FAV_FILE, "r") as f:
        return json.load(f)


def save_favorites(data):
    with open(FAV_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ------------------- HTML -------------------
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NekoBot API Görsel Uygulaması</title>

<style>
    body {
        margin: 0;
        padding: 0;
        background: #0a0a0a;
        color: white;
        font-family: Arial, sans-serif;
        text-align: center;
    }

    h1 {
        margin-top: 20px;
        color: #ff4db8;
        text-shadow: 0 0 10px #ff0099;
    }

    .box {
        width: 95%;
        max-width: 520px;
        background: #1a1a1a;
        margin: auto;
        margin-top: 20px;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 0 20px rgba(255, 0, 150, 0.5);
    }

    select, button {
        width: 100%;
        padding: 14px;
        margin-top: 10px;
        border-radius: 10px;
        font-size: 16px;
        border: none;
    }

    select {
        background: #262626;
        color: white;
        border: 2px solid #ff3399;
    }

    button {
        background: #ff0077;
        color: white;
        font-size: 18px;
        cursor: pointer;
        border: none;
    }

    button:hover {
        background: #ff3399;
    }

    img.single-img {
        width: 100%;
        border-radius: 14px;
        margin-top: 15px;
    }

    .loading {
        display: none;
        margin-top: 10px;
        font-size: 18px;
        color: #ff66cc;
    }

    /* GALERİ GRID */
    #multiGallery {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
        margin-top: 20px;
    }

    .gallery-item {
        position: relative;
    }

    .gallery-img {
        width: 100%;
        border-radius: 12px;
    }

    /* ÇÖP KUTUSU ve FAVORİ BUTONU */
    .delete-btn {
        position: absolute;
        top: 6px;
        right: 6px;
        background: rgba(0,0,0,0.6);
        padding: 6px;
        border-radius: 50%;
        cursor: pointer;
        font-size: 18px;
    }

    .fav-add-btn {
        position: absolute;
        top: 6px;
        right: 44px;
        background: rgba(0,0,0,0.6);
        padding: 6px;
        border-radius: 50%;
        cursor: pointer;
        font-size: 18px;
    }

    /* FULLSCREEN MODAL */
    #modal {
        position: fixed;
        display: none;
        top: 0; 
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.9);
        justify-content: center;
        align-items: center;
        z-index: 999;
    }

    #modal img {
        max-width: 95%;
        max-height: 95%;
        border-radius: 14px;
    }

    .top-buttons {
        position: fixed;
        top: 10px;
        right: 10px;
    }
    .fav-btn {
        background: #ff0088;
        padding: 10px 14px;
        border-radius: 10px;
        font-size: 14px;
        cursor: pointer;
        border: none;
        color: white;
    }
</style>
</head>

<body>

<div class="top-buttons">
    <button class="fav-btn" onclick="goFavs()">⭐ Favoriler</button>
</div>

<h1>NekoBot Görsel Sistemi</h1>

<div class="box">
    <label for="type">Kategori Seç:</label>
    <select id="type">
        <option value="hass">hass</option>
        <option value="hmidriff">hmidriff</option>
        <option value="pgif">pgif</option>
        <option value="4k">4k</option>
        <option value="hentai">hentai</option>
        <option value="holo">holo</option>
        <option value="hneko">hneko</option>
        <option value="neko">neko</option>
        <option value="hkitsune">hkitsune</option>
        <option value="kemonomimi">kemonomimi</option>
        <option value="anal">anal</option>
        <option value="hanal">hanal</option>
        <option value="gonewild">gonewild</option>
        <option value="kanna">kanna</option>
        <option value="ass">ass</option>
        <option value="pussy">pussy</option>
        <option value="thigh">thigh</option>
        <option value="hthigh">hthigh</option>
        <option value="gah">gah</option>
        <option value="coffee">coffee</option>
        <option value="food">food</option>
        <option value="paizuri">paizuri</option>
        <option value="tentacle">tentacle</option>
        <option value="boobs">boobs</option>
        <option value="hboobs">hboobs</option>
        <option value="yaoi">yaoi</option>
        <option value="yuri">yuri</option>
        <option value="blowjob">blowjob</option>
        <option value="cum">cum</option>
        <option value="creampie">creampie</option>
        <option value="bikini">bikini</option>
        <option value="ecchi">ecchi</option>
        <option value="ero">ero</option>
        <option value="feet">feet</option>
        <option value="futa">futa</option>
        <option value="futa_on_female">futa_on_female</option>
        <option value="glasses">glasses</option>
        <option value="lolicon">lolicon</option>
        <option value="masturbation">masturbation</option>
        <option value="neko_gif">neko_gif</option>
        <option value="nekomimi">nekomimi</option>
        <option value="oral">oral</option>
        <option value="petplay">petplay</option>
        <option value="r34">r34</option>
        <option value="schoolgirl">schoolgirl</option>
        <option value="smile">smile</option>
        <option value="spank">spank</option>
        <option value="squirt">squirt</option>
        <option value="swimsuit">swimsuit</option>
        <option value="uniform">uniform</option>
        <option value="vibrator">vibrator</option>
        <option value="wap">wap</option>
        <option value="wallpaper">wallpaper</option>
        <option value="zettai">zettai</option>
    </select>

    <button onclick="getSingle()">Tek Görsel Getir</button>
    <button onclick="getMultiple()">15 Görsel Getir</button>

    <div class="loading" id="loading">Yükleniyor...</div>

    <img id="singleImg" class="single-img" src="" style="display:none;">
    
    <button id="favSingleBtn" style="display:none; margin-top:10px;" class="fav-btn"
        onclick="addFavorite(singleImg.src)">⭐ Favoriye Ekle</button>

    <div id="multiGallery"></div>
</div>

<!-- FULLSCREEN MODAL -->
<div id="modal" onclick="closeModal()">
    <img id="modalImg">
</div>


<script>
// Kısa DOM refs
const loading = document.getElementById("loading");
const singleImg = document.getElementById("singleImg");
const favSingleBtn = document.getElementById("favSingleBtn");
const modal = document.getElementById("modal");
const modalImg = document.getElementById("modalImg");
const multiGallery = document.getElementById("multiGallery");

function goFavs(){ window.location = "/favorites"; }

// FULLSCREEN AÇ
function openModal(src) {
    modalImg.src = src;
    modal.style.display = "flex";
}

// FULLSCREEN KAPAT
function closeModal() {
    modal.style.display = "none";
}


// TEKLİ GÖRSEL
function getSingle() {
    let type = document.getElementById("type").value;

    loading.style.display = "block";

    fetch("/single?type=" + encodeURIComponent(type))
        .then(r => r.json())
        .then(data => {
            singleImg.src = data.image;
            singleImg.style.display = "block";
            favSingleBtn.style.display = "block";
            singleImg.onclick = () => openModal(data.image);
            loading.style.display = "none";
        }).catch(err=>{
            loading.style.display = "none";
            alert("Hata: " + err);
        });
}


// 15 GÖRSEL
function getMultiple() {
    let type = document.getElementById("type").value;
    multiGallery.innerHTML = "";
    loading.style.display = "block";

    fetch("/multi?type=" + encodeURIComponent(type))
        .then(r => r.json())
        .then(data => {

            data.images.forEach(src => {
                let box = document.createElement("div");
                box.className = "gallery-item";

                let img = document.createElement("img");
                img.src = src;
                img.className = "gallery-img";
                img.onclick = () => openModal(src);

                let del = document.createElement("div");
                del.className = "delete-btn";
                del.innerHTML = "🗑";
                del.onclick = () => box.remove();

                let fav = document.createElement("div");
                fav.className = "fav-add-btn";
                fav.innerHTML = "⭐";
                fav.onclick = () => addFavorite(src);

                box.appendChild(img);
                box.appendChild(del);
                box.appendChild(fav);
                multiGallery.appendChild(box);
            });

            loading.style.display = "none";
        }).catch(err=>{
            loading.style.display = "none";
            alert("Hata: " + err);
        });
}

function addFavorite(src){
    fetch("/add_fav", {
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body: JSON.stringify({ image: src })
    }).then(resp => {
        if(resp.ok) alert("Favorilere eklendi!");
        else alert("Favori eklenirken hata.");
    }).catch(e=>{
        alert("Favori eklenemedi: " + e);
    });
}
</script>

</body>
</html>
"""

# ------------------- FAVORİLER SAYFASI -------------------
FAV_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Favoriler</title>

<style>
    body { background:#0a0a0a; color:white; text-align:center; font-family:Arial; }

    .top-buttons {
        margin-top:20px;
    }
    .btn {
        background:#ff0088; padding:12px 18px; border-radius:10px;
        font-size:18px; cursor:pointer; border:none; color:white;
        margin:5px;
    }

    #gallery {
        margin-top:20px;
        display:grid;
        grid-template-columns:repeat(2, 1fr);
        gap:12px;
        padding:10px;
    }
    .item { position:relative; }
    img { width:100%; border-radius:10px; }

    .remove-btn {
        position:absolute; top:6px; right:6px;
        background:rgba(0,0,0,0.6); padding:6px;
        border-radius:50%; cursor:pointer;
    }
</style>

</head>
<body>

<h1>⭐ Favorilerim</h1>

<div class="top-buttons">
    <button class="btn" onclick="home()">🏠 Ana Sayfa</button>
</div>

<div id="gallery"></div>

<script>
function home(){ window.location = "/"; }

fetch("/get_favs")
    .then(r=>r.json())
    .then(data=>{
        let gallery = document.getElementById("gallery");
        data.favorites.forEach(src=>{
            let box = document.createElement("div");
            box.className="item";

            let img = document.createElement("img");
            img.src = src;
            img.onclick = ()=>{ window.open(src, "_blank"); }

            let del = document.createElement("div");
            del.className="remove-btn";
            del.innerHTML="❌";
            del.onclick = ()=>{
                fetch("/remove_fav",{
                    method:"POST",
                    headers:{ "Content-Type":"application/json" },
                    body: JSON.stringify({ image: src })
                }).then(()=>{
                    box.remove();
                });
            }

            box.appendChild(img);
            box.appendChild(del);
            gallery.appendChild(box);
        });
    });
</script>

</body>
</html>
"""

# ------------------- ROUTES -------------------

@app.route("/")
def index():
    return Response(HTML_PAGE, mimetype="text/html")


@app.route("/single")
def single():
    t = request.args.get("type", "neko")
    r = requests.get(f"https://nekobot.xyz/api/image?type={t}").json()
    return jsonify({"image": r.get("message", "")})


@app.route("/multi")
def multi():
    t = request.args.get("type", "neko")
    imgs = []
    for _ in range(15):
        r = requests.get(f"https://nekobot.xyz/api/image?type={t}").json()
        imgs.append(r.get("message", ""))
    return jsonify({"images": imgs})


# -------- FAVORİ İŞLEMLERİ --------

@app.route("/add_fav", methods=["POST"])
def add_fav():
    img = request.json.get("image")
    if not img:
        return jsonify({"ok": False, "error": "no image"}), 400
    favs = load_favorites()
    if img not in favs:
        favs.append(img)
    save_favorites(favs)
    return jsonify({"ok": True})


@app.route("/get_favs")
def get_favs():
    return jsonify({"favorites": load_favorites()})


@app.route("/remove_fav", methods=["POST"])
def remove_fav():
    img = request.json.get("image")
    if not img:
        return jsonify({"ok": False, "error": "no image"}), 400
    favs = load_favorites()
    if img in favs:
        favs.remove(img)
    save_favorites(favs)
    return jsonify({"ok": True})


@app.route("/favorites")
def favorites_page():
    return Response(FAV_HTML, mimetype="text/html")


# ------------------- RUN -------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)