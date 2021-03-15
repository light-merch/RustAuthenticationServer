import json
import uuid
import hashlib

import flask

app = flask.Flask(__name__)

users = dict()
userspath = "users.json"
try:
    with open(userspath, "r") as usersfile:
        users = json.load(usersfile)
except:
    print("Database not found")

@app.route("/")
def root():
    return "Authentication server is running!"

@app.route("/register", methods=["GET", "POST"])
def register():
    data = flask.request.form.to_dict()
    hashedpass = hashlib.sha256(bytearray(data["passwd"], "UTF-8")).hexdigest()
    users[data["username"]] = dict({"passwd": hashedpass,
                                    "email": data["email"],
                                    "auth": None})
    with open(userspath, "w") as usersfile:
        print(json.dump(users, usersfile, indent=4))
    return "ok"

@app.route("/login", methods=["GET", "POST"])
def login():
    data = flask.request.form.to_dict()
    print(data)
    if users[data["username"]]["passwd"] == hashlib.sha256(bytearray(data["passwd"], "UTF-8")).hexdigest():
        if(users[data["username"]]["auth"] is None):
            users[data["username"]]["auth"] = uuid.uuid4().hex
        return users[data["username"]]["auth"]
    return None

@app.route("/logout", methods=["GET", "POST"])
def logout():
    data = flask.request.form.to_dict()
    print(users[data["username"]]["auth"], data["auth"])
    if users[data["username"]]["auth"] == data["auth"]:
        users[data["username"]]["auth"] = None
    return "ok"

if __name__ == "__main__":
    app.run(host="192.168.1.40", port="40500", ssl_context=("ssl/server.cert", "ssl/server.key"))