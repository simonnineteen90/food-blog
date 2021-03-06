from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/login', methods=["POST"])
def receive_data():
    username = request.form["username"]
    password = request.form["password"]
    return f"You logged in with the username {username} and password {password}"



if __name__ == "__main__":
    app.run(debug=True)