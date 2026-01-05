# 🎬 Video İndirici (GUI)

Modern arayüzlü, **yt-dlp + FFmpeg** tabanlı; YouTube, Shorts, TikTok ve Instagram Reels için **video & MP3 indirici**.

> ⚠️ **FFmpeg ZORUNLUDUR.** Uygulama FFmpeg olmadan çalışmaz.

---

## ✨ Özellikler

* 🎥 Video indirme (720p – 1080p – 4K – **8K (mevcutsa)**)
* 🎵 MP3 ses indirme
* 📦 Toplu link desteği (alt alta yapıştır)
* 🖥️ Modern GUI (CustomTkinter)
* 🚀 Hızlı & stabil (yt-dlp)
* 🪟 Windows uyumlu

---

## 🧰 Gereksinimler

* **Python 3.10+**
* **FFmpeg (zorunlu)**
* Windows işletim sistemi

Python paketleri:

```bash
pip install yt-dlp customtkinter
```

---

## ⚙️ FFmpeg Kurulumu (ZORUNLU)

### 📥 1. FFmpeg indir

Resmi site:
👉 [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

Windows için **static build** indir.

---

### 📂 2. Proje içine yerleştir

FFmpeg klasör yapısı **AŞAĞIDAKİ GİBİ OLMALI**:

```
video-indirici/
│
├─ ffmpeg/
│  └─ bin/
│     ├─ ffmpeg.exe
│     ├─ ffplay.exe
│     └─ ffprobe.exe
│
├─ main.py
└─ ...
```

> ❗ `ffmpeg.exe` mutlaka `ffmpeg/bin` içinde olmalı.

Uygulama çalışırken FFmpeg yolunu **otomatik algılar**:

* Normal çalışmada: proje dizininden
* Build (exe) halinde: `_MEIPASS` içinden

---

## ▶️ Çalıştırma

```bash
python main.py
```

---

## 🏗️ Build (EXE) Alma

### 1️⃣ PyInstaller kur

```bash
pip install pyinstaller
```

### 2️⃣ Build al

```bash
pyinstaller --onefile --noconsole \
  --add-data "ffmpeg;ffmpeg" \
  main.py
```

📌 Build sonrası `dist/main.exe` oluşur.

> ⚠️ `--add-data "ffmpeg;ffmpeg"` **olmazsa FFmpeg çalışmaz**.

---

## 🧠 Teknik Notlar

* FFmpeg yolu kod içinde otomatik belirlenir:

  * `sys._MEIPASS` (build)
  * `__file__` (normal çalışma)
* 8K seçilse bile **gerçek 8K yoksa**, mevcut en yüksek kalite indirilir
* İndirme işlemleri **thread** ile yapılır (arayüz donmaz)

---

## 📸 Desteklenen Platformlar

* YouTube (Video & Shorts)
* TikTok
* Instagram Reels

---

## 👤 Geliştirici

**Egemen AL**
GitHub: [https://github.com/LXDEZ31](https://github.com/LXDEZ31)

---

## ⚠️ Yasal Uyarı

Bu proje **eğitim amaçlıdır**.
İndirilen içeriklerin kullanımından **kullanıcı sorumludur**.

---

⭐ Repo hoşuna gittiyse yıldız atmayı unutma
