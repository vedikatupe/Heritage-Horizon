from flask import Flask, render_template

app = Flask(
    __name__,
    template_folder="../FRONTEND",
    static_folder="../FRONTEND"
)

# ---------------- SPLASH / TITLE PAGE ----------------
@app.route("/")
def splash():
    return render_template("TITLEPAGE.HTML")


# ---------------- COMMON FLOW ----------------
@app.route("/slide")
def slide():
    return render_template("SLIDE2.HTML")

@app.route("/login")
def login():
    return render_template("FSLOGIN.HTML")

@app.route("/dashboard")
def dashboard():
    return render_template("DASHBOARD.HTML")


# ---------------- UNIVERSE MODULE ----------------
@app.route("/universe/quiz")
def universe_quiz():
    return render_template("solarquiz.html")

@app.route("/universe/asteroid")
def universe_asteroid():
    return render_template("solarasteriod.html")

@app.route("/universe/wordpuzzle")
def universe_wordpuzzle():
    return render_template("solarwordpuzzle.html")

@app.route("/universe/crush")
def universe_crush():
    return render_template("solarcrush.html")

@app.route("/universe/doyouknow")
def universe_doyouknow():
    return render_template("solardoyouknow.html")


# ---------------- HERITAGE MODULE ----------------
@app.route("/heritage/wordpuzzle")
def heritage_wordpuzzle():
    return render_template("wordpuzzleH.html")

@app.route("/heritage/maze")
def heritage_maze():
    return render_template("IND_FinalMaze1.html")

@app.route("/heritage/quiz")
def heritage_quiz():
    return render_template("IND_finalQuiz.html")

@app.route("/heritage/cards")
def heritage_cards():
    return render_template("InFINALCARD.html")


if __name__ == "__main__":
    app.run(debug=True)
