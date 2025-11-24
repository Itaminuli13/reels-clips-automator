import os
import random
import time
import requests
from datetime import datetime
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip, ColorClip
from instagrapi import Client

# لاگین
cl = Client()
cl.delay_range = [3, 10]
cl.load_settings("session.json")
try:
    cl.get_timeline_feed()
    print("لاگین شد")
except Exception as e:
    print("session خراب:", e)
    exit()

# لینک بک‌گراند خفن (همیشه سالم، 9:16، نئون + پارتیکل)
BG_URL = "https://www.pexels.com/download/video/8501993/"

captions = [
    "The future of AI is here — and it's insane",
    "ChatGPT just changed everything forever",
    "Grok 4 just dropped. Elon broke the internet again",
    "Neuralink started human trials. This is not sci-fi anymore",
    "Tesla Bot now walks better than most humans",
    "Quantum computing is no longer theory — it's 2025",
    "Web3 isn't coming. It's already here",
    "Apple Vision Pro just killed the smartphone era",
    "Bitcoin to $150K? The bull run just started",
    "AI agents are replacing jobs in 2026 — are you ready?",
]

hashtags = " #AI #Tech #Future #Viral"

def download_bg():
    try:
        print("در حال دانلود بک‌گراند خفن...")
        r = requests.get(BG_URL, stream=True, timeout=30)
        r.raise_for_status()
        with open("bg.mp4", "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print("بک‌گراند دانلود شد")
        return "bg.mp4"
    except Exception as e:
        print("دانلود نشد، استفاده از صفحه رنگی:", e)
        return None

def post_reel():
    caption = random.choice(captions) + hashtags
    ts = datetime.now().strftime("%H-%M")
    audio_file = f"voice_{ts}.mp3"
    output_video = f"reel_{ts}.mp4"

    print(f"در حال ساخت ریلز: {caption[:60]}...")

    # صدا
    gTTS(text=caption, lang='en', slow=False).save(audio_file)

    # بک‌گراند
    bg_path = download_bg()
    try:
        if bg_path and os.path.getsize(bg_path) > 1000000:  # حداقل 1MB
            bg = VideoFileClip(bg_path).subclip(0, 20)
        else:
            raise Exception("فایل خراب")
    except:
        print("بک‌گراند خراب بود — استفاده از صفحه رنگی خفن")
        duration = AudioFileClip(audio_file).duration + 2
        bg = ColorClip(size=(1080,1920), color=(10,0,40), duration=duration)  # بنفش تیره خفن

    # ترکیب
    voice = AudioFileClip(audio_file)
    final = bg.set_audio(voice)
    final = final.subclip(0, min(15, voice.duration + 2))

    final.write_videofile(
        output_video,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        threads=2,
        logger=None,
        verbose=False
    )

    # آپلود
    try:
        cl.clip_upload(output_video, caption=caption)
        print(f"ریلز خفن رفت بالا! {datetime.now().strftime('%H:%M')}")
    except Exception as e:
        print("آپلود نشد:", str(e)[:100])

    # پاکسازی
    for f in [audio_file, output_video, "bg.mp4"]:
        if os.path.exists(f):
            os.remove(f)

# شروع
if __name__ == "__main__":
    print("ربات ریلز حرفه‌ای شروع شد — هر ۴ ساعت یه ریلز خفن")
    while True:
        try:
            post_reel()
        except Exception as e:
            print("خطا داد ولی ادامه می‌دیم:", e)
        print("۴ ساعت دیگه...")
        time.sleep(4 * 60 * 60)
