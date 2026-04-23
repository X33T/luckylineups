from flask import Flask, render_template, request
from generator import generate_teams

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    teams = []

    if request.method == "POST":
        num = int(request.form["num"])
        mode = request.form["mode"]

        teams = generate_teams(num, mode)

    return render_template("index.html", teams=teams)


if __name__ == "__main__":
    app.run(debug=True)