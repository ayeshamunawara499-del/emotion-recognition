def get_suggestion(emotion):

    suggestions = {
        "happy": "Keep smiling!",
        "sad": "Take a short break.",
        "angry": "Take a deep breath.",
        "fear": "Stay calm. You can do it.",
        "surprise": "Enjoy the moment.",
        "neutral": "Have a wonderful day.",
        "disgust": "Relax and stay positive."
    }

    return suggestions.get(emotion, "Have a nice day!")