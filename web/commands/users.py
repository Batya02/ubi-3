from objects import globals
from objects.globals import app, ip_adress, admin_password
from flask import render_template, request

from db_models.User import User

@app.route("/users", methods=["GET", "POST"])
async def users():

    if request.cookies.get("username") != admin_password:
        return '<a href="/login">Go to login</a>'
    
    if bool(request.form.get("sort-users")):
        if not globals.in_users:
            globals.in_users = True
            globals.users = await User.objects.all()
            globals.count_users = len(globals.users)
        else:
            globals.in_users = False
            globals.users = reversed(globals.users)
    else:
        globals.users = await User.objects.all()
        globals.count_users = len(globals.users)

    return render_template(
        "users.html",        users=globals.users, 
        ip_adress=ip_adress, count_users=globals.count_users
        )