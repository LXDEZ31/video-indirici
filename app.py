import customtkinter as ctk
from tkinter import filedialog, messagebox
import yt_dlp
import os
import sys
import threading

def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    ffmpeg_path = os.path.join(base_path, "ffmpeg", "bin")
    
    ffmpeg_exe = os.path.join(ffmpeg_path, "ffmpeg.exe")
    if not os.path.exists(ffmpeg_exe):
        messagebox.showerror("FFmpeg Hatası", "FFmpeg bulunamadı! Lütfen ffmpeg klasörünü kontrol edin.")
    
    return ffmpeg_path

FFMPEG_PATH = get_ffmpeg_path()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class VideoDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Video Downloader Pro")
        self.geometry("1200x780")
        self.resizable(False, False)

        title = ctk.CTkLabel(self, text="Video Downloader", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=(25, 5))
        subtitle = ctk.CTkLabel(self, text="YouTube, Shorts, TikTok, Reels & MP3 indirici (8K Destekli)", text_color="gray")
        subtitle.pack(pady=(0, 15))

        self.tabview = ctk.CTkTabview(self, width=680, height=500)
        self.tabview.pack(pady=10, padx=10, fill="both", expand=True)

        self.video_tab = self.tabview.add("Video")
        self.audio_tab = self.tabview.add("Ses (MP3)")
        self.settings_tab = self.tabview.add("Ayarlar")

        self.create_video_tab()
        self.create_audio_tab()
        self.create_settings_tab()

        signature = ctk.CTkLabel(self, text="Made by Egemen AL", text_color="#777", font=ctk.CTkFont(size=11, slant="italic"))
        signature.place(relx=1.0, rely=1.0, x=-12, y=-10, anchor="se")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.save_path.set(folder)
            self.path_label.configure(text=f"Kayıt yeri: {folder}")

    def create_video_tab(self):
        self.save_path = ctk.StringVar(value=os.getcwd())
        self.path_label = ctk.CTkLabel(self.video_tab, text=f"Kayıt yeri: {self.save_path.get()}")
        self.path_label.pack(pady=(15,5))

        self.path_button = ctk.CTkButton(self.video_tab, text="Klasör Seç", command=self.select_folder)
        self.path_button.pack(pady=5)

        ctk.CTkLabel(self.video_tab, text="Platform Seç:").pack(pady=(10, 2))
        self.platform = ctk.StringVar(value="YouTube Video")
        self.platform_menu = ctk.CTkOptionMenu(
            self.video_tab, variable=self.platform,
            values=["YouTube Video", "YouTube Shorts", "Instagram Reels", "TikTok"]
        )
        self.platform_menu.pack(pady=5)

        ctk.CTkLabel(self.video_tab, text="Video Kalitesi:").pack(pady=(10, 2))
        self.quality = ctk.StringVar(value="En Yüksek (8K)")
        self.quality_menu = ctk.CTkOptionMenu(
            self.video_tab, variable=self.quality,
            values=["En Yüksek (8K)", "4K", "1080p", "720p"]
        )
        self.quality_menu.pack(pady=5)

        warning_label = ctk.CTkLabel(
            self.video_tab, 
            text="8K indirme: Gerçek 8K içerikler sınırlıdır. Maksimum mevcut kalite indirilir",
            text_color="orange",
            font=ctk.CTkFont(size=11)
        )
        warning_label.pack(pady=(5, 10))

        self.video_links = ctk.CTkTextbox(self.video_tab, width=600, height=120)
        self.video_links.insert("0.0", "Bir veya birden fazla video linkini alt alta gir...\n")
        self.video_links.pack(pady=10)

        self.video_progress = ctk.CTkProgressBar(self.video_tab, width=500)
        self.video_progress.pack(pady=5)
        self.video_progress.set(0)
        self.progress_text = ctk.CTkLabel(self.video_tab, text="0%")
        self.progress_text.pack()

        self.video_download_button = ctk.CTkButton(self.video_tab, text="Videoları İndir", command=self.start_video_thread)
        self.video_download_button.pack(pady=15)

        self.status_label_video = ctk.CTkLabel(self.video_tab, text="")
        self.status_label_video.pack(pady=5)

    def create_audio_tab(self):
        self.audio_links = ctk.CTkTextbox(self.audio_tab, width=600, height=120)
        self.audio_links.insert("0.0", "Bir veya birden fazla linki alt alta gir (sadece ses olarak indirilecek)...\n")
        self.audio_links.pack(pady=10)

        self.audio_progress = ctk.CTkProgressBar(self.audio_tab, width=500)
        self.audio_progress.pack(pady=5)
        self.audio_progress.set(0)
        self.audio_percent = ctk.CTkLabel(self.audio_tab, text="0%")
        self.audio_percent.pack()

        self.audio_download_button = ctk.CTkButton(self.audio_tab, text="MP3 Olarak İndir", command=self.start_audio_thread)
        self.audio_download_button.pack(pady=15)

        self.status_label_audio = ctk.CTkLabel(self.audio_tab, text="")
        self.status_label_audio.pack(pady=5)


    def create_settings_tab(self):
        ctk.CTkLabel(self.settings_tab, text="FFmpeg Yolu:", font=ctk.CTkFont(weight="bold")).pack(pady=(25, 5))
        ctk.CTkLabel(self.settings_tab, text=FFMPEG_PATH, wraplength=500, text_color="gray").pack(pady=5)

    def start_video_thread(self):
        threading.Thread(target=self.download_videos, daemon=True).start()

    def start_audio_thread(self):
        threading.Thread(target=self.download_audios, daemon=True).start()

    def progress_hook_video(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0%').replace('%', '').strip()
            try:
                self.video_progress.set(float(percent) / 100)
                self.progress_text.configure(text=f"{percent}%")
            except:
                pass
        elif d['status'] == 'finished':
            self.video_progress.set(1)
            self.progress_text.configure(text="Tamamlandı")

    def progress_hook_audio(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0%').replace('%', '').strip()
            try:
                self.audio_progress.set(float(percent) / 100)
                self.audio_percent.configure(text=f"{percent}%")
            except:
                pass
        elif d['status'] == 'finished':
            self.audio_progress.set(1)
            self.audio_percent.configure(text="Tamamlandı")

    def download_videos(self):
        links = [line.strip() for line in self.video_links.get("0.0", "end").splitlines() if line.strip()]
        if not links:
            messagebox.showwarning("Hata", "Lütfen en az bir link gir!")
            return

        quality_map = {
            "720p": "best[height<=720]",
            "1080p": "best[height<=1080]",
            "4K": "best[height<=2160]",
            "En Yüksek (8K)": "best[height>=4320]/best[height>=2880]/best[height>=2160]/best[height>=1440]/best[height>=1080]/best"
        }

        self.video_progress.set(0)
        self.progress_text.configure(text="0%")

        for url in links:
            self.status_label_video.configure(text=f"İndiriliyor: {url}", text_color="yellow")
            self.update()

            try:
                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    formats = info.get('formats', [])
                    
                    available_resolutions = set()
                    max_height = 0
                    
                    print("=" * 50)
                    print(f"Video: {info.get('title', 'Bilinmeyen')}")
                    print("Mevcut formatlar:")
                    
                    for f in formats:
                        height = f.get('height', 0)
                        if height:
                            available_resolutions.add(height)
                            max_height = max(max_height, height)
                            vcodec = f.get('vcodec', 'bilinmiyor')
                            acodec = f.get('acodec', 'ses yok')
                            format_note = f.get('format_note', '')
                            print(f"  {height}p - Video: {vcodec} - Ses: {acodec} - {format_note}")
                    
                    print(f"Maksimum bulunan çözünürlük: {max_height}p")
                    print("=" * 50)
                    
                    if self.quality.get() == "En Yüksek (8K)" and max_height < 4320:
                        self.status_label_video.configure(
                            text=f"8K bulunamadı. Maksimum {max_height}p indiriliyor...", 
                            text_color="orange"
                        )
                    
            except Exception as e:
                print(f"Video bilgisi alınamadı: {e}")

            ydl_opts = {
                'outtmpl': os.path.join(self.save_path.get(), '%(title)s.%(ext)s'),
                'format': quality_map[self.quality.get()],
                'merge_output_format': 'mp4',
                'noplaylist': True,
                'quiet': False,
                'ffmpeg_location': FFMPEG_PATH,
                'progress_hooks': [self.progress_hook_video],
                'extractaudio': False,
                'keepvideo': True,
                'writethumbnail': False,
            }

            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }]

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                self.status_label_video.configure(text="İndirme tamamlandı", text_color="lightgreen")
                
                messagebox.showinfo("Başarılı", f"Video başarıyla indirildi!\n\nKayıt yeri: {self.save_path.get()}")
                
            except Exception as e:
                error_msg = f"Hata: {str(e)}"
                print(error_msg)
                self.status_label_video.configure(text=error_msg, text_color="red")
                messagebox.showerror("İndirme Hatası", f"İndirme sırasında hata:\n{str(e)}")

    def download_audios(self):
        links = [line.strip() for line in self.audio_links.get("0.0", "end").splitlines() if line.strip()]
        if not links:
            messagebox.showwarning("Hata", "Lütfen en az bir link gir!")
            return

        self.audio_progress.set(0)
        self.audio_percent.configure(text="0%")

        for url in links:
            self.status_label_audio.configure(text=f"İndiriliyor: {url}", text_color="yellow")
            self.update()

            ydl_opts = {
                'outtmpl': os.path.join(os.getcwd(), '%(title)s.%(ext)s'),
                'format': 'bestaudio/best',
                'noplaylist': True,
                'quiet': True,
                'ffmpeg_location': FFMPEG_PATH,
                'progress_hooks': [self.progress_hook_audio],
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                self.status_label_audio.configure(text="Ses indirildi", text_color="lightgreen")
            except Exception as e:
                self.status_label_audio.configure(text=f"Hata: {e}", text_color="red")


if __name__ == "__main__":
    app = VideoDownloaderApp()
    app.mainloop()