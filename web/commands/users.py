from objects import globals
from objects.globals import app, ip_adress, admin_password
from flask import render_template, request

from requests import get

from db_models.User import User

@app.route("/users", methods=["GET", "POST"])
async def users():

    ip_addr = request.environ.get("HTTP_X_FORWARDED_FOR")

    if request.cookies.get("username") != admin_password:
        return '<a href="/login">Go to login</a>'
    
    if bool(request.form.get("sort-users")):
        globals.users = list(reversed(globals.users))
    else:
        globals.users = await User.objects.all()
        globals.count_users = len(globals.users)

    return render_template(
        "users.html",        users=globals.users, 
        ip_adress=ip_addr, count_users=globals.count_users
        )