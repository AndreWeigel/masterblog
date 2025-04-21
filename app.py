from flask import Flask, render_template, request, redirect, url_for

from blog_manager import BlogManager, BlogPost


BLOG_POSTS_FILE = "blog_posts.json"
app = Flask(__name__)


@app.route('/')
def index():
    blog = BlogManager(BLOG_POSTS_FILE)
    blog_posts = blog.get_all_posts()
    blog_posts.reverse()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        blog = BlogManager(BLOG_POSTS_FILE)
        blog.add_post(BlogPost(author, title, content))

        return redirect(url_for('index'))
    return render_template('add.html')


if __name__ == '__main__':
    app.run()
