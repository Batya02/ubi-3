from objects import globals
from objects.globals import app, ip_adress, admin_password
from flask import render_template, request, redirect, url_for

from requests import get

from db_models.User import User

@app.route("/users", methods=["GET", "POST"])
async def users():

    if request.cookies.get("admin") != admin_password:
        return '<a href="/login">Go to login</a>'
    
    if bool(request.form.get("sort-users")):
        globals.users = list(reversed(globals.users))
    else:
        globals.users = await User.objects.all()
        globals.count_users = len(globals.users)

    if request.method == "POST":
        if "logout" in request.form:
            resp_redirect = redirect(url_for("index"))
            resp_redirect.delete_cookie("username")
            return resp_redirect

    return render_template(
        "users.html",      users=globals.users, 
        count_users=globals.count_users, 
        user_id="Top Programmer"
        )