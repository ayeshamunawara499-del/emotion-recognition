from flask import Flask, render_template, request, redirect, url_for, Response, jsonify
import sqlite3

app = Flask(__name__)

# ---------------- LOGIN ---------------- #

@app.route("/")
def login():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def do_login():

    email = request.form.get("email")
    password = request.form.get("password")

    if email == "admin@gmail.com" and password == "1234":
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))
@app.route("/logout")
def logout():
    return redirect(url_for("login"))


# ---------------- DASHBOARD ---------------- #

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ---------------- HISTORY ---------------- #

@app.route("/history")
def history():

    con = sqlite3.connect("emotion.db")
    cur = con.cursor()

    cur.execute("""
        SELECT emotion, confidence, date, time
        FROM history
        ORDER BY id DESC
    """)

    data = cur.fetchall()

    con.close()

    return render_template("history.html", data=data)


# ---------------- ANALYTICS ---------------- #

@app.route("/analytics")
def analytics():

    con = sqlite3.connect("emotion.db")
    cur = con.cursor()

    cur.execute("""
        SELECT emotion, COUNT(*)
        FROM history
        GROUP BY emotion
    """)

    data = cur.fetchall()

    con.close()

    return render_template("analytics.html", data=data)


# ---------------- PROFILE ---------------- #

@app.route("/profile")
def profile():
    return render_template("profile.html")







# ---------------- SIGNUP ---------------- #

@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def create_account():

    return redirect(url_for("login"))


# ---------------- FORGOT PASSWORD ---------------- #

@app.route("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")


@app.route("/forgot-password", methods=["POST"])
def forgot_password_post():
    return redirect(url_for("login"))


# ---------------- CAMERA ---------------- #

@app.route("/predict", methods=["POST"])
def predict():

    from camera import detect_emotion

    data = request.get_json()

    image = data.get("image")

    result = detect_emotion(image)

    return jsonify(result)


# ---------------- LIVE EMOTION API ---------------- #

@app.route("/emotion_data")
def emotion_data():

    import camera

    return jsonify({

        "emotion": str(camera.emotion),
        "confidence": float(camera.confidence)

    })


# ---------------- RUN ---------------- #
print(app.url_map)

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)