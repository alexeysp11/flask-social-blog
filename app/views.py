from flask import render_template, url_for, request, flash, redirect
from flask_login import current_user
from app import app
from app.auth.views import auth_blueprint
from app.user.views import user_blueprint
from app.posts.views import posts_blueprint


app.register_blueprint(auth_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(posts_blueprint)


@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated: 
        return redirect(url_for('posts.feed'))
    
    else:
        img_follow = url_for('static', 
                        filename='pictures/follow_your_interests.png')
        img_hear = url_for('static', 
                        filename='pictures/hear_what_people_talking_about.png')
        img_join = url_for('static', 
                        filename='pictures/join_the_conversation.png')
        
        return render_template('main/home.html', 
                                img_follow=img_follow, 
                                img_hear=img_hear,
                                img_join=img_join)


@app.route("/about")
def about():
    return render_template('main/about.html')


@app.errorhandler(404)
def error404(e):
    return render_template('main/error404.html')
