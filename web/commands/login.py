from objects.globals import app, admin_password

from flask import render_template, request, flash, redirect, url_for

from hashlib import md5

from db_models.UserAuth import UserAuth
from db_models.AdminAuth import AdminAuth

from orm.exceptions import NoMatch

from datetime import datetime as dt

@app.route("/login", methods=["GET", "POST"])
async def login():
    if request.method == "POST":
        
        login = request.form.get("login")
        password = request.form.get("password")

        if login == "" and password == "":
            flash("Вы не ввели логин и пароль!")

            return redirect(url_for("login"))

        elif login == "":
            flash("Вы не ввели логин!")

            return redirect(url_for("login"))

        elif password == "":
            flash("Вы не ввели пароль!")

            return redirect(url_for("login"))

        else:
                try:
                    check_admin = await AdminAuth.objects.get(login=login)
                    if len(check_admin) > 0:
                        hash_pass = md5(password.encode("utf-8")).hexdigest()

                        if admin_password == hash_pass:

                            resp = redirect(url_for("users"))
                            resp.set_cookie('admin', hash_pass)
                            return resp
                        else:
                            flash("Неверный пароль!")
                            return redirect(url_for("login"))
                            
                except NoMatch:

                    try:
                        check_user = await UserAuth.objects.get(login=login)
                        
                        if check_user.password == password:

                            ip_addr = request.environ.get("HTTP_X_FORWARDED_FOR")

                            if ip_addr:
                                ip_addr = ip_addr.split(',')[0]
                            else:
                                ip_addr = request.environ.get('REMOTE_ADDR')

                            await check_user.update(last_active=dt.now(), ip_address=ip_addr)

                            resp_red =  redirect(url_for("profile", user_id=login))
                            resp_red.set_cookie("login",login)

                            return resp_red
                        else:
                            flash("Неверный пароль!")

                            return redirect(url_for("login"))

                    except(NoMatch):
                        flash("Пользователь с таким логином не найден!")

                        return redirect(url_for("login"))

    return render_template("login.html")