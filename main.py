# main.py - Instagram Reels Auto-Poster (Based on eddieoz/reels-clips-automator + Instagrapi)
# Global English Version - Viral Tech & AI Reels every 4 hours

import os
import random
import time
from datetime import datetime
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from instagrapi import Client

# ==================== FILES (باید توی ریپو باشن) ====================
BACKGROUND_VIDEO = "background.mp4"      # ← حتماً آپلود کن (9:16, 15–60 ثانیه)
SESSION_FILE = "session.json"           # ← همونی که لوکال ساختی

# ==================== Instagram Login with Session ====================
cl = Client()
cl.delay_range = [2, 8]  # ضد بن

if not os.path.exists(SESSION_FILE):
    print("ERROR: session.json not found! Upload it!")
    exit()

cl.load_settings(SESSION_FILE)
try:
    cl.get_timeline_feed()
    print("Logged in successfully with session.json")
except Exception as e:
    print("Session expired:", e)
    exit()

# ==================== Viral Tech/AI Topics (English) ====================
TOPICS = [
    "AI", "ChatGPT", "Neuralink", "Grok 4", "Quantum Computing",
    "Self-Driving Cars", "Metaverse", "Web3", "Crypto Crash", "Apple Vision Pro",
    "Tesla Robot", "SpaceX Starship", "6G Technology", "Brain-Computer Interface"
]

CAPTION_TEMPLATES = [
    "This {topic} update just broke the internet!",
    "The future of {topic} is here — and it's insane!",
    "You NEED to see this {topic} breakthrough!",
    "Why {topic} will dominate 2026",
    "Mind officially blown by {topic}!",
    "This changes everything in {topic} forever"
]

HASHTAGS = " #AI #Tech #Technology #Viral #FYP #Trending #Future #Innovation"

# ==================== Reel Creation + Upload ====================
def create_and_upload():
    topic = random.choice(TOPICS)
    template = random.choice(CAPTION_TEMPLATES)
    caption = template.format(topic=topic) + HASHTAGS

    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    voice_file = f"voice_{ts}.mp3"
    output_file = f"reel_{ts}.mp4"

    print(f"Creating reel about: {topic}")
    print(f"Caption: {caption}")

    # 1. TTS (English)
    tts = gTTS(text=caption, lang='en', slow=False)
    tts.save(voice_file)

    # 2. Background video (loop to 30s)
    bg = VideoFileClip(BACKGROUND_VIDEO).loop(duration=35).subclip(0, 35)

    # 3. Voiceover
    voice = AudioFileClip(voice_file)
    bg = bg.set_audio(voice)

    # 4. Big viral text overlay (exact style of eddieoz — super viral!)
    txt = TextClip(topic.upper(),
                   fontsize=100,
                   color='white',
                   font='Impact',
                   stroke_color='black',
                   stroke_width=6)
    txt = txt.set_position('center').set_duration(6).set_start(1.5)

    final = CompositeVideoClip([bg, txt]).subclip(0, min(29, voice.duration + 4))

    # 5. Export
    final.write_videofile(output_file, fps=30, codec="libx264", audio_codec="aac", threads=4)
    print("Video generated!")

    # 6. Upload to Instagram Reels
    try:
        cl.clip_upload(output_file, caption=caption)
        print(f"REEL UPLOADED SUCCESSFULLY! {ts} 🚀")
    except Exception as e:
        print("Upload failed:", e)

    # Clean up
    for f in [voice_file, output_file]:
        if os.path.exists(f):
            os.remove(f)

# ==================== Run Forever (every 4 hours) ====================
if __name__ == "__main__":
    print("AI Reels Bot Started — Global Version (eddieoz style + Instagrapi)")
    while True:
        try:
            create_and_upload()
        except Exception as e:
            print("Error:", e)
        
        print("Sleeping 4 hours... Next reel coming soon!")
        time.sleep(4 * 60 * 60)  # ۴ ساعت
