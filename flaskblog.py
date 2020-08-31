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
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)