from flask import Flask, render_template, request, redirect, url_for, session
from questions import QUESTIONS, NAMES

app = Flask(__name__)
app.secret_key = "поменяй-на-любую-длинную-фразу"


@app.route("/")
def index():
    session.clear()
    return render_template("index.html")


@app.route("/start")
def start():
    session["scores"] = {key: 0 for key in NAMES}
    session["current"] = 0
    return redirect(url_for("question"))


@app.route("/question", methods=["GET", "POST"])
def question():
    if "scores" not in session:
        return redirect(url_for("index"))

    current = session["current"]

    if request.method == "POST":
        answer_number = int(request.form["answer"])
        answer = QUESTIONS[current]["answers"][answer_number]
        scores = session["scores"]
        for key, points in answer["points"].items():
            scores[key] += points
        session["scores"] = scores
        session["current"] = current + 1
        if session["current"] >= len(QUESTIONS):
            return redirect(url_for("result"))
        return redirect(url_for("question"))

    return render_template(
        "question.html",
        q=QUESTIONS[current],
        number=current + 1,
        total=len(QUESTIONS),
    )


@app.route("/result")
def result():
    if "scores" not in session:
        return redirect(url_for("index"))
    scores = session["scores"]
    top = sorted(scores, key=scores.get, reverse=True)
    return render_template(
        "result.html",
        first=NAMES[top[0]],
        second=NAMES[top[1]],
    )


if __name__ == "__main__":
    app.run(debug=True)
