from flask import Flask, render_template, request, redirect, url_for
import smtplib
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
# DB SETUP
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food-blog.db'
db = SQLAlchemy(app)

# CREATE DB TABLE
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(150), nullable=False)
    content = db.Column(db.String(250), nullable=False)
    ingredients = db.Column(db.String(250), nullable=False)
    method = db.Column(db.String(500), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    


db.create_all()    


# CONTACT FORM EMAIL
def send_email(name, email, message):
    my_email = "appdunntest@gmail.com"
    password = "password goes here"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user= my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=my_email,
                            msg=f"Subject: Contact form \n\n Name: {name} \n Email: {email} \n Message: {message}")

# @app.route('/contact')
# def contact():
#     return render_template('index.html')


@app.route('/')
def index():
    all_posts = db.session.query(Post).all()
    return render_template('index.html', posts=all_posts)

@app.route('/post')
def post():
    post_id = request.args.get('id')
    post_to_edit = Post.query.get(post_id)
    ingredients = post_to_edit.ingredients.split(";")
    method = post_to_edit.method.split(";")
    
    return render_template('post.html', post=post_to_edit, ingredients=ingredients, method=method)    

@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        name = request.form["contact_name"]
        email = request.form["contact_email"]
        message = request.form["contact_message"]
        send_email(name, email, message)
        return render_template('contact.html', msg_sent=True)
    return render_template('contact.html', msg_sent=False)



## DB ROUTES

# VIEW ALL POSTS
@app.route('/all_posts')
def all_posts():
    all_posts = db.session.query(Post).all()
    return render_template('all_posts.html', posts=all_posts) 

# ADD NEW POST TO DB
@app.route('/add_post', methods=['POST', 'GET'])
def add_post():
    if request.method == "POST":
        new_post = Post(
            heading=request.form["heading"],
            content=request.form["content"],
            ingredients=request.form["ingredients"],
            method=request.form["method"],
            difficulty=request.form["difficulty"]
        )
        db.session.add(new_post)
        db.session.commit()
        # print([new_post.heading, new_post.content,new_post.ingredients,new_post.difficulty])
        return redirect(url_for('all_posts'))

    # all_posts = db.session.query(Post).all()
    # return render_template('add_post.html', posts=all_posts) 
    return render_template('add_post.html') 
     

# DELETE A POST
@app.route('/delete_post')
def delete_post():
    # this gets the id from the argument passed in the url_for in the html template
    post_id = request.args.get('id')

    post_to_delete = Post.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('all_posts'))

# EDIT A POST
@app.route('/edit_post', methods=['POST','GET'])
def edit_post():
    # gets the id from the argument in the url_for in html doc
    post_id = request.args.get('id')
    post_to_edit = Post.query.get(post_id)

    print(post_id)
    print(post_to_edit)


    ## IF request is POST (when the form is submitted)
    if request.method == "POST":
        
        # get the id of post to be edited
        id = request.form["id"]
        print(id)
        
        # access the db entry
        post_to_update = Post.query.get(id)    

        # set the new content for the post
        # book_to_update.rating = request.form["rating"]

        post_to_update.heading = request.form["heading"]
        post_to_update.content = request.form["content"]
        post_to_update.ingredients = request.form["ingredients"]
        post_to_update.difficulty = request.form["difficulty"]

        # # commit the changes
        db.session.commit()

        # reuturn a html page
        return redirect(url_for('all_posts'))     

    return render_template('edit_post.html', post=post_to_edit)




if __name__ == "__main__":
    app.run(debug=True)