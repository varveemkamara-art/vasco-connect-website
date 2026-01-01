from flask import Flask, render_template, request, redirect, url_for, session, flash
import smtplib

app = Flask(__name__)
app.secret_key = "vasco_secret_key"  # Keep this secret

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

# In-memory storage for requests
requests_list = []

# Home page / form submission
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        service = request.form.get("service")

        # Save request
        requests_list.append({
            "name": name,
            "phone": phone,
            "service": service
        })

        # Send email notification
        try:
            sender_email = "vascobusinessconnecthub@gmail.com"
            sender_password = "qrcukngpgfnacbls"  # App password
            receiver_email = "vascobusinessconnecthub@gmail.com"

            message = f"""Subject: New Service Request

Name: {name}
Phone: {phone}
Service: {service}
"""

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, message)
        except Exception as e:
            print("Email sending failed:", e)

        flash("Request submitted successfully!")
        return redirect(url_for("success"))

    return render_template("index.html")


# Success page after submission
@app.route("/success")
def success():
    return render_template("success.html")


# Admin login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            flash("Login successful!")
            return redirect(url_for("admin"))
        else:
            flash("Invalid login credentials")
            return redirect(url_for("login"))

    return render_template("login.html")


# Admin dashboard
@app.route("/admin")
def admin():
    if not session.get("admin"):
        flash("Please login first")
        return redirect(url_for("login"))

    return render_template("admin.html", data=requests_list)


# Delete request by index
@app.route("/delete/<int:item_id>")
def delete(item_id):
    if not session.get("admin"):
        flash("Please login first")
        return redirect(url_for("login"))

    if 0 <= item_id < len(requests_list):
        removed = requests_list.pop(item_id)
        flash(f"Deleted request from {removed['name']}")

    return redirect(url_for("admin"))


# Logout
@app.route("/logout")
def logout():
    session.pop("admin", None)
    flash("Logged out successfully")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
