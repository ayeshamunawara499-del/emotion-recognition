const startBtn = document.getElementById("start-camera");

const emotionName = document.getElementById("emotion-name");
const emotionConfidence = document.getElementById("emotion-confidence");

const confidenceText = document.getElementById("confidence-text");
const confidenceBar = document.getElementById("confidence-bar");

const aiSuggestion = document.getElementById("ai-suggestion");

const totalDetection = document.getElementById("total-detection");

const happyCount = document.getElementById("happy-count");
const sadCount = document.getElementById("sad-count");
const neutralCount = document.getElementById("neutral-count");

let total = 0;
let happy = 0;
let sad = 0;
let neutral = 0;
let lastEmotion = "";

if (startBtn) {

    startBtn.addEventListener("click", () => {

        startBtn.innerHTML = "Camera Running";

        startBtn.style.background = "#16a34a";

    });

}

async function updateEmotion() {

    try {

        const response = await fetch("/emotion_data");

        const data = await response.json();

        emotionName.innerHTML = data.emotion;

        emotionConfidence.innerHTML =
            data.confidence.toFixed(1) + "%";

        confidenceText.innerHTML =
            data.confidence.toFixed(1) + "%";

        confidenceBar.style.width =
            data.confidence + "%";

        // ------------------------
        // AI Suggestion
        // ------------------------

        switch (data.emotion) {

            case "happy":

                aiSuggestion.innerHTML =
                    "😊 Keep Smiling!";

                break;

            case "sad":

                aiSuggestion.innerHTML =
                    "❤️ Take some rest.";

                break;

            case "angry":

                aiSuggestion.innerHTML =
                    "😌 Relax and breathe.";

                break;

            case "fear":

                aiSuggestion.innerHTML =
                    "💙 Stay Calm.";

                break;

            case "surprise":

                aiSuggestion.innerHTML =
                    "😄 Great Reaction!";

                break;

            default:

                aiSuggestion.innerHTML =
                    "🙂 Stay Positive.";

        }

        // ------------------------
        // Analytics Counter
        // ------------------------

        if (
            data.emotion !== "Waiting..." &&
            data.emotion !== lastEmotion
        ) {

            total++;

            totalDetection.innerHTML = total;

            if (data.emotion === "happy") {

                happy++;

                happyCount.innerHTML = happy;

            }

            else if (data.emotion === "sad") {

                sad++;

                sadCount.innerHTML = sad;

            }

            else if (data.emotion === "neutral") {

                neutral++;

                neutralCount.innerHTML = neutral;

            }

            lastEmotion = data.emotion;

        }

    }

    catch (err) {

        console.log(err);

    }

}

setInterval(updateEmotion, 1000);