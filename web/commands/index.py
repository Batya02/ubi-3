from objects.globals import app, ip_adress, admin_password
from flask import render_template, request, redirect, url_for

@app.route("/", methods=["GET", "POST"])
async def index():
    
    ip_addr = request.environ.get("HTTP_X_FORWARDED_FOR")

    if ip_addr:
        ip_addr = ip_addr.split(',')[0]
    else:
        ip_addr = request.environ.get('REMOTE_ADDR')

    user_resp_cookie = request.cookies.get("login")
    admin_resp_cookie = request.cookies.get("admin")

    if user_resp_cookie != None:
        return redirect(url_for("profile", user_id=int(user_resp_cookie)))
    
    elif admin_resp_cookie != None:
        return redirect(url_for("users"))
    
    if request.method == "POST":
        return redirect(url_for("login"))

    return render_template("index.html", ip_adress=ip_adress)