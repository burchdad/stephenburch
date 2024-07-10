from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_bcrypt import Bcrypt # type: ignore
from dotenv import load_dotenv # type: ignore
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
bcrypt = Bcrypt(app)

POSTS_DIR = '_posts'

# Replace this with a hashed password stored in an environment variable
hashed_password = os.getenv('HASHED_PASSWORD')

@app.route('/')
def home():
    return "Hello, this is the home page."

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and bcrypt.check_password_hash(hashed_password, password):
            session['logged_in'] = True
            return redirect(url_for('update'))
    return render_template('login.html')

@app.route('/admin')
def admin():
    if 'logged_in' in session:
        return render_template('admin.html')
    return redirect(url_for('login'))

@app.route('/update', methods=['GET', 'POST'])
def update():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        categories = request.form['categories']
        content = request.form['content']

        filename = f"{date}-{title.replace(' ', '-').lower()}.md"
        filepath = os.path.join(POSTS_DIR, filename)

        with open(filepath, 'w') as file:
            file.write(f"---\n")
            file.write(f"title: \"{title}\"\n")
            file.write(f"date: {date}\n")
            file.write(f"categories: {categories}\n")
            file.write(f"---\n\n")
            file.write(content)

        return jsonify({"message": "Blog post submitted successfully!"})

    return render_template('update.html')

@app.route('/submit-blog-post', methods=['POST'])
def submit_blog_post():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
        
    title = request.form['title']
    date = request.form['date']
    categories = request.form['categories']
    content = request.form['content']

    filename = f"{date}-{title.replace(' ', '-').lower()}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    with open(filepath, 'w') as file:
        file.write(f"---\n")
        file.write(f"title: \"{title}\"\n")
        file.write(f"date: {date}\n")
        file.write(f"categories: {categories}\n")
        file.write(f"---\n\n")
        file.write(content)

    return jsonify({"message": "Blog post submitted successfully!"})

if __name__ == '__main__':
    if not os.path.exists(POSTS_DIR):
        os.makedirs(POSTS_DIR)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
