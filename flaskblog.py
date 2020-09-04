from flask import Flask, render_template

app = Flask(__name__)

posts = [
    {
        'author': 'Alex', 
        'title': 'Blog post 1',
        'content': 'First post content', 
        'date_posted': 'July 15, 2020'
    }, 
    {
        'author': 'Simon', 
        'title': 'Blog post 2',
        'content': 'Second post content', 
        'date_posted': 'July 15, 2020'
    }, 
    {
        'author': 'Frank', 
        'title': 'Blog post 3',
        'content': 'Third post content', 
        'date_posted': 'July 16, 2020'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/profile")
def profile():
    return render_template('profile.html', posts=posts)

@app.route("/feed")
def feed():
    return render_template('feed.html', posts=posts)

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/forgot_password")
def forgot_password():
    return render_template('forgot_password.html')

@app.route("/new")
def new():
    return render_template('new.html')

if __name__ == '__main__':
    app.run(debug=True)