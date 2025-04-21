from flask import Flask, render_template, request

from blog_manager import BlogManager

app = Flask(__name__)


@app.route('/')
def index():
    blog = BlogManager()
    blog_posts = blog.get_all_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # We will fill this in the next step
        pass
    return render_template('add.html')


if __name__ == '__main__':
    app.run()
