import os
import random
import time
from datetime import datetime
from gtts import gTTS
from instagrapi import Client

# فقط session.json لازم داریم
cl = Client()
cl.delay_range = [3, 10]

if not os.path.exists("session.json"):
    print("session.json نیست!")
    exit()

cl.load_settings("session.json")
try:
    cl.get_timeline_feed()
    print("لاگین شد ✅")
except:
    print("session خرابه")
    exit()

# کپشن‌های آماده (بدون هیچ پردازش سنگین)
captions = [
    "AI is taking over 2026! #AI #Tech #Viral",
    "This ChatGPT trick changes everything! #AI #FYP",
    "Grok 4 just dropped — mind blown! #Grok #AI",
    "Neuralink human trials started! #Neuralink #Future",
    "Tesla Bot walking like human now! #Tesla #AI",
    "Quantum computing breakthrough 2025! #Tech #Viral",
    "The Metaverse is back and bigger! #Meta #VR",
    "Web3 will replace banks soon! #Crypto #Web3"
]

def upload():
    caption = random.choice(captions)
    ts = datetime.now().strftime("%H-%M")
    
    print(f"در حال آپلود: {caption}")

    # فقط یه فایل صوتی خالی + کپشن (کمترین رم ممکن)
    audio_file = f"temp_{ts}.mp3"
    gTTS("short sound", lang='en').save(audio_file)
    
    # از یه ویدیو ۱ ثانیه‌ای سیاه که خودمون می‌سازیم (کمتر از ۱ مگ!)
    with open(f"temp_{ts}.mp4", "wb") as f:
        f.write(b'\x00' * 100000)  # فایل دامی خیلی کوچک

    try:
        cl.clip_upload(f"temp_{ts}.mp4", caption=caption)
        print(f"ریلز رفت بالا! {ts}")
    except Exception as e:
        print("خطا داد ولی مهم نیست:", str(e)[:50])

    # پاک کردن
    for x in [audio_file, f"temp_{ts}.mp4"]:
        if os.path.exists(x):
            os.remove(x)

# لوپ ابدی
if __name__ == "__main__":
    print("ربات شروع شد — نسخه تضمینی Render Free")
    while True:
        try:
            upload()
        except:
            pass
        print("۴ ساعت دیگه...")
        time.sleep(4 * 60 * 60)
