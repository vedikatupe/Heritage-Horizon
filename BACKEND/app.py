from flask import Flask, render_template

app = Flask(__name__, template_folder="../FRONTEND", static_folder="../FRONTEND")

@app.route("/login")
def login():
    return render_template("FSLOGIN.html")   # <-- updated to actual file

@app.route("/titlepage")
def titlepage():
    return render_template("titlepage.html")

@app.route("/slide")
def slide():
    return render_template("slide 2.html")

@app.route("/quiz")
def quiz():
    return render_template("IND_finalQuiz.html")  # <-- updated

if __name__ == "__main__":
    app.run(debug=True)