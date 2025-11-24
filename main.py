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
if not os.path.exists("session.json"):
    print("session.json نیست!")
    exit()
cl.load_settings("session.json")
try:
    cl.get_timeline_feed()
    print("لاگین شد ✅")
except Exception as e:
    print("session خراب:", e)
    exit()

# کپشن‌های وایرال
captions = [
    "AI is taking over 2026! #AI #Tech #Viral #FYP",
    "ChatGPT just got 100x smarter! #AI #ChatGPT #Trending",
    "Grok 4 is here! #Grok #ElonMusk",
    "Neuralink first human trials! #Neuralink #Future",
    "Tesla Bot walking like human! #Tesla #AI",
    "Quantum computing breakthrough! #Tech #2025",
    "Web3 is the future! #Crypto #Web3"
]

def download_bg():
    # URL جدید از جستجو (سالم و 9:16 tech)
    url = "https://videos.pexels.com/video-files/8549029/8549029-uhd_3840_2160_30fps.mp4"  # Tech abstract background
    try:
        r = requests.get(url, stream=True, timeout=30)
        r.raise_for_status()
        with open("bg_temp.mp4", 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        if os.path.exists("bg_temp.mp4") and os.path.getsize("bg_temp.mp4") > 5000000:  # حداقل 5MB
            print("بک‌گراند دانلود شد")
            return "bg_temp.mp4"
    except Exception as e:
        print("دانلود خطا:", e)
    return None

def post():
    caption = random.choice(captions)
    ts = datetime.now().strftime("%H-%M")
    audio_file = f"audio_{ts}.mp3"
    output = f"reel_{ts}.mp4"

    print(f"ساخت ریلز: {caption}")

    # صدا
    gTTS(caption, lang='en').save(audio_file)

    # بک‌گراند
    bg_file = download_bg()
    if bg_file:
        try:
            bg = VideoFileClip(bg_file).subclip(0, 15)
            audio = AudioFileClip(audio_file)
            final = bg.set_audio(audio)
            final = final.subclip(0, min(14, audio.duration + 1))
            final.write_videofile(output, fps=24, codec="libx264", audio_codec="aac",
                                  preset="ultrafast", threads=1, logger=None, verbose=False)
            os.remove(bg_file)
            print("ویدیو با بک‌گراند ساخته شد")
        except Exception as e:
            print("خطا در ویدیو:", e)
            # fallback
            audio = AudioFileClip(audio_file)
            duration = min(14, audio.duration + 1)
            final = ColorClip(size=(1080, 1920), color=(10, 20, 50), duration=duration)
            final = final.set_audio(audio)
            final.write_videofile(output, fps=24, codec="libx264", audio_codec="aac",
                                  preset="ultrafast", threads=1, logger=None, verbose=False)
            print("fallback به صفحه رنگی")
    else:
        # fallback
        audio = AudioFileClip(audio_file)
        duration = min(14, audio.duration + 1)
        final = ColorClip(size=(1080, 1920), color=(10, 20, 50), duration=duration)
        final = final.set_audio(audio)
        final.write_videofile(output, fps=24, codec="libx264", audio_codec="aac",
                              preset="ultrafast", threads=1, logger=None, verbose=False)
        print("fallback به صفحه رنگی")

    # آپلود (حل validation error با extra_data)
    try:
        cl.clip_upload(
            output,
            caption=caption,
            extra_data={"clips_metadata": {"original_sound_info": {"original_sound_id": "0"}}}
        )
        print(f"ریلز رفت بالا! {ts}")
    except Exception as e:
        print("آپلود خطا:", str(e)[:60])

    # پاک کردن
    for f in [audio_file, output]:
        if os.path.exists(f): os.remove(f)

if __name__ == "__main__":
    print("ربات شروع شد — نسخه با fallback و حل validation")
    while True:
        try:
            post()
        except Exception as e:
            print("خطا:", e)
        print("۴ ساعت دیگه...")
        time.sleep(4 * 60 * 60)
