from objects.globals import app, ip_adress, admin_password
from flask import render_template, request

@app.route("/", methods=["GET", "POST"])
async def index():
    if request.cookies.get("username") != admin_password:
        return '<a href="/login">Go to login</a>'

    return render_template("index.html", ip_adress=ip_adress)