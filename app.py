from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("skillswap.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            return redirect(f"/dashboard/{user[1]}")
        else:
            return "❌ Invalid Email or Password"

    return render_template("login.html")


# ---------------- SIGNUP ----------------

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        regno = request.form["regno"]
        email = request.form["email"]
        password = request.form["password"]
        teach = request.form["teach"]
        learn = request.form["learn"]

        conn = sqlite3.connect("skillswap.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users
            (name, regno, email, password, teach, learn)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, regno, email, password, teach, learn))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")


# ---------------- DASHBOARD ----------------

@app.route("/dashboard/<username>")
def dashboard(username):
    return render_template(
        "dashboard.html",
        username=username
    )


# ---------------- PROFILE ----------------

@app.route("/profile/<username>")
def profile(username):

    conn = sqlite3.connect("skillswap.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, regno, email, teach, learn FROM users WHERE name=?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return render_template(
            "profile.html",
            username=username,
            name=user[0],
            regno=user[1],
            email=user[2],
            teach=user[3],
            learn=user[4]
        )

    return "User not found"


# ---------------- SKILL MATCHING ----------------
@app.route("/matching/<username>")
def matching(username):

    conn = sqlite3.connect("skillswap.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Current user's details
    cursor.execute(
        "SELECT * FROM users WHERE name=?",
        (username,)
    )

    current_user = cursor.fetchone()

    if not current_user:
        conn.close()
        return "User not found"

    # Other users
    cursor.execute(
        "SELECT * FROM users WHERE name != ?",
        (username,)
    )

    users = cursor.fetchall()

    conn.close()

    matches = []

    # Match:
    # My learning skill == Other person's teaching skill
    for user in users:

        if current_user["learn"].lower() in user["teach"].lower():

            matches.append(user)

    return render_template(
        "matching.html",
        username=username,
        matches=matches
    )


# ---------------- REQUESTS ----------------

# Supports BOTH:
# /requests
# /requests/sriraksha

@app.route("/requests")
@app.route("/requests/<username>")
def requests(username=None):

    return render_template(
        "requests.html",
        username=username
    )


# ---------------- ACCEPT REQUEST ----------------

@app.route("/accept_request", methods=["POST"])
def accept_request():

    person = request.form.get("person")
    username = request.form.get("username", "sriraksha")

    print("Request accepted from:", person)

    return redirect(f"/requests/{username}")


# ---------------- REJECT REQUEST ----------------

@app.route("/reject_request", methods=["POST"])
def reject_request():

    person = request.form.get("person")
    username = request.form.get("username", "sriraksha")

    print("Request rejected from:", person)

    return redirect(f"/requests/{username}")


# ---------------- SEND REQUEST ----------------

@app.route("/send_request", methods=["POST"])
def send_request():

    person = request.form.get("person")
    username = request.form.get("username", "sriraksha")

    print("Request sent to:", person)

    return redirect(f"/requests/{username}")


# ---------------- FEEDBACK ----------------

@app.route("/feedback/<username>", methods=["GET", "POST"])
def feedback(username):

    if request.method == "POST":

        name = request.form["name"]
        rating = request.form["rating"]
        feedback_text = request.form["feedback"]

        print("Feedback:", name, rating, feedback_text)

        return redirect(f"/dashboard/{username}")

    return render_template("feedback.html", username=username)


@app.route("/feedback/submit", methods=["POST"])
def submit_feedback():

    name = request.form.get("name")
    rating = request.form.get("rating")
    feedback_text = request.form.get("feedback")

    print("Feedback:")
    print("Name:", name)
    print("Rating:", rating)
    print("Feedback:", feedback_text)

    username = request.form.get("username", "sriraksha")

    return redirect(f"/dashboard/{username}")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    return redirect("/login")


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)