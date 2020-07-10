# flask app

from flask import Flask, render_template

from line import script, div, cdn_js, cdn_css

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", script=script, div=div, cdn_js=cdn_js, cdn_css=cdn_css)


if __name__ == "__main__":
    app.run(debug=True)
