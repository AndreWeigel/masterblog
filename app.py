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


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    blog = BlogManager(BLOG_POSTS_FILE)
    success = blog.delete_post(post_id)
    if success:
        print("Post deleted successfully!", "success")
    else:
        print("Post not found!")
    return redirect(url_for('index'))

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    blog = BlogManager(BLOG_POSTS_FILE)
    post = blog.get_post(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        blog.update_post(post_id, BlogPost(author, title, content, _id = post_id))
        print(f"Post with id {post_id} updated successfully!",)

        return redirect(url_for('index'))
    return render_template('edit.html', post=post)

if __name__ == '__main__':
    app.run()
