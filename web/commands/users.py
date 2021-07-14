from objects.globals import app, ip_adress
from flask import render_template, request

from db_models.User import User

@app.route("/users", methods=["GET", "POST"])
async def users():

    users = await User.objects.all()

    return render_template("users.html", users=users, ip_adress=ip_adress)