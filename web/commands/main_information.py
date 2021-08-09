from objects.globals import app

from flask import request, render_template, redirect, url_for

from db_models.UserAuth import UserAuth

@app.route("/profile/<int:user_id>/main_info/", methods=["GET", "POST"])
async def main_info(user_id):
    if request.cookies.get("login") == None:
        return redirect(url_for("index"))

    if request.method == "POST":
        if "logout" in request.form:
            resp_redirect = redirect(url_for("index"))
            resp_redirect.delete_cookie("login")
            return resp_redirect

    main_data = await UserAuth.objects.get(login=user_id)

    return render_template("main_information.html", user_id=user_id, main_data=main_data, title="Main Information")

@app.errorhandler(404)
def not_found(e):   
    return redirect(url_for("index"))