from objects.globals import app, ip_adress
from flask import render_template

@app.route("/", methods=["GET", "POST"])
async def index():
    return render_template("index.html", ip_adress=ip_adress)