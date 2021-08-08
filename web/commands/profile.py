from objects import globals
from objects.globals import app, admin_password
from flask import render_template, request, redirect, url_for

from requests import get

from db_models.User import User

@app.route("/profile/<int:user_id>", methods=["GET", "POST"])
async def profile(user_id):
    if request.method == "POST":
        if "logout" in request.form:
            resp_redirect = redirect(url_for("index"))
            resp_redirect.delete_cookie("login")
            return resp_redirect
    return render_template("profile.html", title="My Profile", user_id=user_id)