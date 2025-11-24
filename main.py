# main.py - Ultra-light version for Render Free tier (≤512MB RAM)
import os
import random
import time
from datetime import datetime
from gtts import gTTS
from moviepy.editor import ColorClip, AudioFileClip, concatenate_videoclips
from instagrapi import Client

# فایل‌ها
SESSION_FILE = "session.json"
AUDIO_ONLY = True  # فقط صدا + صفحه رنگی (رم خیلی کم می‌خوره)

# لاگین
cl = Client()
cl.delay_range = [3, 9]
if not os.path.exists(SESSION_FILE):
    print("session.json not found!")
    exit()
cl.load_settings(SESSION_FILE)
try:
    cl.get_timeline_feed()
    print("Logged in with session.json")
except Exception as e:
    print("Session error:", e)
    exit()

# موضوعات انگلیسی وایرال
TOPICS = ["AI", "ChatGPT", "Grok", "Neuralink", "Tesla Bot", "Quantum AI", "Web3", "Metaverse"]
CAPTIONS = [
    "This {t} update is INSANE!",
    "The future of {t} just arrived!",
    "Mind blown by {t} breakthrough!",
    "Why {t} will dominate 2026",
    "{t} just changed everything!"
]
HASHTAGS = " #AI #Tech #Viral #FYP #Trending"

def create_reel():
    topic = random.choice(TOPICS)
    caption = random.choice(CAPTIONS).format(t=topic) + HASHTAGS
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    audio_file = f"audio_{ts}.mp3"
    video_file = f"reel_{ts}.mp4"

    print(f"Topic: {topic} | {caption}")

    # ۱. فقط صدا بساز (gTTS خیلی سبک)
    tts = gTTS(caption, lang='en', slow=False)
    tts.save(audio_file)

    # ۲. ویدیو فقط یه صفحه رنگی + صدا (بدون background.mp4 → ۴۰۰ مگ رم صرفه‌جویی!)
    audio = AudioFileClip(audio_file)
    duration = audio.duration + 1

    clip = ColorClip(size=(1080, 1920), color=(10, 20, 40)).set_duration(duration)  # آبی تیره
    clip = clip.set_audio(audio)
    clip.write_videofile(video_file, fps=24, codec="libx264", audio_codec="aac", verbose=False, logger=None)

    # ۳. آپلود
    try:
        cl.clip_upload(video_file, caption=caption)
        print(f"REEL UPLOADED! {ts}")
    except Exception as e:
        print("Upload error:", e)

    # پاکسازی
    for f in [audio_file, video_file]:
        if os.path.exists(f): os.remove(f)

# لوپ اصلی
if __name__ == "__main__":
    print("Ultra-light Reels Bot Started (Render Free tier)")
    while True:
        try:
            create_reel()
        except Exception as e:
            print("Error:", e)
        print("Next reel in 4 hours...")
        time.sleep(4 * 60 * 60)
