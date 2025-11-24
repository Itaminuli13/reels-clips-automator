import os
import random
import time
from datetime import datetime
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
from instagrapi import Client

# لاگین
cl = Client()
cl.delay_range = [3, 10]
cl.load_settings("session.json")
try:
    cl.get_timeline_feed()
    print("لاگین شد")
except:
    print("session خرابه")
    exit()

# کپشن‌های وایرال
captions = [
    "AI is taking over 2026! #AI #Tech #Viral #FYP",
    "ChatGPT just got 100x smarter! #AI #ChatGPT #Trending",
    "Grok 4 dropped — mind blown! #Grok #ElonMusk",
    "Neuralink first human trials started! #Neuralink #Future",
    "Tesla Bot walks like human now! #Tesla #AI #Robotics",
    "Quantum computing is here! #Tech #2025",
    "Web3 will replace banks! #Crypto #Web3 #Blockchain"
]

def post():
    caption = random.choice(captions)
    ts = datetime.now().strftime("%H-%M")
    audio_file = f"audio_{ts}.mp3"
    output = f"reel_{ts}.mp4"

    print(f"ساخت ریلز: {caption}")

    # صدا
    gTTS(caption, lang='en', slow=False).save(audio_file)

    # ویدیو بک‌گراند + صدا (سبک‌ترین روش ممکن)
    bg = VideoFileClip("tech_background.mp4").subclip(0, 15)  # فقط 15 ثانیه اول
    audio = AudioFileClip(audio_file)
    final = bg.set_audio(audio)
    final = final.subclip(0, min(14, audio.duration + 1))  # حداکثر 14 ثانیه
    final.write_videofile(output, fps=24, codec="libx264", audio_codec="aac",
                          preset="ultrafast", threads=2, logger=None, verbose=False)

    # آپلود
    try:
        cl.clip_upload(output, caption=caption)
        print(f"ریلز رفت بالا! {ts}")
    except Exception as e:
        print("آپلود نشد:", str(e)[:50])

    # پاک کردن فایل‌ها
    for f in [audio_file, output]:
        if os.path.exists(f): os.remove(f)

if __name__ == "__main__":
    print("ربات شروع شد — نسخه ویدیویی + بک‌گراند (100% کار می‌کنه)")
    while True:
        try:
            post()
        except Exception as e:
            print("یه خطا داد ولی ادامه می‌دیم:", e)
        print("۴ ساعت دیگه...")
        time.sleep(4 * 60 * 60)
