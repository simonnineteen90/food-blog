from flask import Flask, render_template, request
import smtplib


def send_email(name, email, message):
    my_email = "appdunntest@gmail.com"
    password = "password goes here"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user= my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=my_email,
                            msg=f"Subject: Contact form \n\n Name: {name} \n Email: {email} \n Message: {message}")


app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/flex-practice')
def flex_practice():
    return render_template('flex-practice.html')

@app.route('/contact', methods=["POST"])
def contact():
    if request.method == "POST":
        name = request.form["contact_name"]
        email = request.form["contact_email"]
        message = request.form["contact_message"]
        send_email(name, email, message)
        return render_template('index.html', msg_sent=True)
    return render_template('index.html', msg_sent=False)


if __name__ == "__main__":
    app.run(debug=True)