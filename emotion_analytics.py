import pandas as pd
import matplotlib.pyplot as plt

# Read CSV
data = pd.read_csv("emotion_log.csv")

# Remove empty emotions
data = data[data["Emotion"].notna()]
data = data[data["Emotion"] != ""]

# Count emotions
emotion_counts = data["Emotion"].value_counts()

print("\nEmotion Statistics\n")
print(emotion_counts)

# Create Bar Chart
plt.figure(figsize=(8,5))

emotion_counts.plot(
    kind="bar",
    color=[
        "green",
        "blue",
        "red",
        "gray",
        "purple",
        "orange",
        "brown"
    ]
)

plt.title("Emotion Statistics")
plt.xlabel("Emotion")
plt.ylabel("Count")

plt.grid(axis="y", linestyle="--", alpha=0.5)

# Show value on each bar
for i, value in enumerate(emotion_counts.values):
    plt.text(
        i,
        value + 0.3,
        str(value),
        ha="center",
        fontsize=10
    )

plt.tight_layout()
plt.show()