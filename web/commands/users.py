from flask import render_template, request, redirect, url_for

from objects import globals
from objects.globals import app, admin_password
from db_models.UserAuth import UserAuth

@app.route("/users", methods=["GET", "POST"])
async def users():
    if request.cookies.get("admin") != admin_password:
        return redirect(url_for("index"))

    if bool(request.form.get("sort-users")):
        globals.users = list(reversed(globals.users))
    else:
        globals.users = await UserAuth.objects.all()
        globals.count_users = len(globals.users)

    if request.method == "POST":
        if "logout" in request.form:
            resp_redirect = redirect(url_for("index"))
            resp_redirect.delete_cookie("admin")
            return resp_redirect

        elif "more-info" in request.form:
            user_id:int = int(request.form["more-info"])
            return redirect(url_for("more_info", user_id=user_id))

    return render_template(
        "users.html",      users=globals.users, 
        count_users=globals.count_users, 
        web_data = UserAuth)

@app.route("/more-info/<int:user_id>", methods=["GET", "POST"])
async def more_info(user_id):
    main_data_user = await User.objects.get(user_id=user_id)
    web_data_user = await UserAuth.objects.get(login=user_id)

    return render_template("more_info.html", title_user_id=user_id, main_data=main_data_user, web_data=web_data_user)
