from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2

# Load Windows Emoji Font
emoji_font = ImageFont.truetype("seguiemj.ttf", 32)


def get_emoji(emotion):
    emoji_dict = {
        "happy": "😊",
        "sad": "😢",
        "angry": "😡",
        "neutral": "😐",
        "surprise": "😲",
        "fear": "😨",
        "disgust": "🤢"
    }

    return emoji_dict.get(emotion, "🙂")


def draw_emoji(frame, emoji, x, y):

    img = Image.fromarray(
        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    )

    draw = ImageDraw.Draw(img)

    draw.text(
        (x, y),
        emoji,
        font=emoji_font,
        embedded_color=True
    )

    frame[:] = cv2.cvtColor(
        np.array(img),
        cv2.COLOR_RGB2BGR
    )