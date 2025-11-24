import os
import random
import time
from datetime import datetime
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip
from instagrapi import Client

# لاگین
cl = Client()
cl.delay_range = [3, 10]

if not os.path.exists("session.json"):
    print("session.json پیدا نشد!")
    exit()

cl.load_settings("session.json")
try:
    cl.get_timeline_feed()
    print("لاگین شد")
except Exception as e:
    print("session خراب یا بن شدی:", e)
    exit()

# کپشن‌های قوی و تمیز (هشتگ کم و هوشمند)
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

def post_reel():
    caption = random.choice(captions) + hashtags
    ts = datetime.now().strftime("%H-%M")
    audio_file = f"voice_{ts}.mp3"
    output_video = f"reel_{ts}.mp4"

    print(f"در حال ساخت ریلز: {caption[:50]}...")

    # ساخت صدا
    gTTS(text=caption, lang='en', slow=False).save(audio_file)

    # ترکیب با بک‌گراند خفن (فایلی که آپلود کردی)
    bg = VideoFileClip("bg.mp4").loop(duration=20)
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

    # آپلود بدون خطا
    try:
        cl.clip_upload(
            path=output_video,
            caption=caption,
            extra_data={
                "custom_accessibility_caption": "",
                "like_and_view_counts_disabled": False,
                "disable_comments": False,
            }
        )
        print(f"ریلز خفن رفت بالا! {datetime.now().strftime('%H:%M')}")
    except Exception as e:
        print("آپلود نشد:", str(e)[:80])

    # پاکسازی
    for f in [audio_file, output_video]:
        if os.path.exists(f):
            os.remove(f)

# لوپ ابدی
if __name__ == "__main__":
    print("ربات ریلز حرفه‌ای شروع شد — هر ۴ ساعت یه ریلز خفن")
    while True:
        try:
            post_reel()
        except Exception as e:
            print("یه خطا داد ولی ادامه می‌دیم:", e)
        
        print("۴ ساعت دیگه ریلز بعدی...")
        time.sleep(4 * 60 * 60)  # دقیقاً ۴ ساعت
