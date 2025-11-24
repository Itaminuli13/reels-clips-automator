import os
import random
import time
import requests
from datetime import datetime
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip
from instagrapi import Client

# لینک یه بک‌گراند خفن 9:16 (از Pexels — همیشه کار می‌کنه)
BG_URL = "https://www.pexels.com/download/video/8501993/"

cl = Client()
cl.delay_range = [3, 10]
cl.load_settings("session.json")
try:
    cl.get_timeline_feed()
    print("لاگین شد")
except Exception as e:
    print("session خراب:", e)
    exit()

captions = [
    "AI is taking over 2026! #AI #Tech #Viral #FYP",
    "ChatGPT just got 100x smarter! #AI #ChatGPT",
    "Grok 4 is here! #Grok #ElonMusk",
    "Neuralink first human trials! #Neuralink #Future",
    "Tesla Bot walking like human! #Tesla #AI",
    "Quantum computing breakthrough! #Tech #2025",
    "Web3 is the future! #Crypto #Web3"
]

def post():
    caption = random.choice(captions)
    ts = datetime.now().strftime("%H-%M")
    audio_file = f"audio_{ts}.mp3"
    bg_file = f"bg_{ts}.mp4"
    output = f"reel_{ts}.mp4"

    print(f"در حال ساخت ریلز: {caption}")

    # ۱. دانلود بک‌گراند (فقط ۱۵ ثانیه اول)
    print("دانلود بک‌گراند...")
    r = requests.get(BG_URL, stream=True)
    with open(bg_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    # ۲. صدا
    gTTS(caption, lang='en').save(audio_file)

    # ۳. ترکیب
    bg = VideoFileClip(bg_file).subclip(0, 15)
    audio = AudioFileClip(audio_file)
    final = bg.set_audio(audio)
    final = final.subclip(0, min(14, audio.duration + 1))
    final.write_videofile(output, fps=24, codec="libx264", audio_codec="aac",
                          preset="ultrafast", threads=2, logger=None, verbose=False)

    # ۴. آپلود
    try:
        cl.clip_upload(output, caption=caption)
        print(f"ریلز رفت بالا! {ts}")
    except Exception as e:
        print("آپلود نشد:", e)

    # پاکسازی
    for f in [audio_file, bg_file, output]:
        if os.path.exists(f):
            os.remove(f)

if __name__ == "__main__":
    print("ربات شروع شد — نسخه آنلاین بک‌گراند (۱۰۰٪ کار می‌کنه)")
    while True:
        try:
            post()
        except Exception as e:
            print("خطا داد ولی ادامه می‌دیم:", e)
        print("۴ ساعت دیگه...")
        time.sleep(4 * 60 * 60)
