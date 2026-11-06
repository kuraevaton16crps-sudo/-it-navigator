from flask import Flask, render_template, request, redirect, url_for, session
from questions import QUESTIONS, NAMES, INFO

app = Flask(__name__)
app.secret_key = "поменяй-на-любую-длинную-фразу"

MAX_POINTS = {}
for key in NAMES:
    MAX_POINTS[key] = 0
    for q in QUESTIONS:
        best = 0
        for answer in q["answers"]:
            points = answer["points"].get(key, 0)
            if points > best:
                best = points
        MAX_POINTS[key] += best


@app.route("/")
def index():
    session.clear()
    return render_template("index.html", total=len(QUESTIONS), names=NAMES, info=INFO)


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

    percents = {}
    for key in scores:
        percents[key] = round(scores[key] * 100 / MAX_POINTS[key])
    top = sorted(percents, key=percents.get, reverse=True)

    bars = []
    for key in top:
        bars.append({
            "name": NAMES[key],
            "icon": INFO[key]["icon"],
            "color": INFO[key]["color"],
            "percent": percents[key],
        })

    return render_template(
        "result.html",
        first_name=NAMES[top[0]],
        first=INFO[top[0]],
        second_name=NAMES[top[1]],
        second=INFO[top[1]],
        bars=bars,
    )


if __name__ == "__main__":
    app.run(debug=True)
