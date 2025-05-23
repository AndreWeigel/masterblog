# Import necessary modules from Flask
from flask import Flask, render_template, request, redirect, url_for, flash

# Import custom blog manager and post classes
from blog_manager import BlogManager, BlogPost

# Define the file to store blog posts
BLOG_POSTS_FILE = "blog_posts.json"
app = Flask(__name__)
app.secret_key = "masterblog"

# Create instance of blog_manager at module level
blog = BlogManager(BLOG_POSTS_FILE)
# Route for the homepage that displays all blog posts


def validate_post_form(title, author, content):
    errors = []
    if not title:
        errors.append("Title is required.")
    if not author:
        errors.append("Author is required.")
    if not content:
        errors.append("Content is required.")
    return errors


@app.route('/')
def index():
    blog_posts = blog.get_all_posts()
    blog_posts.reverse()
    return render_template('index.html', posts=blog_posts)


# Route to add a new blog post
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        content = request.form.get('content', '').strip()

        errors = validate_post_form(title, author, content)

        if errors:
            for error in errors:
                flash(error)
            return redirect(url_for('add'))
        # Create a new blog post and add it
        if blog.add_post(BlogPost(author, title, content)):
            flash('Post successfully added!')
        else:
            flash('Error adding post. Please try again.')

        return redirect(url_for('index'))
    # Render the form for GET requests
    return render_template('add.html')


# Route to delete a blog post by its ID
@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    success = blog.delete_post(post_id)
    if success:
        flash('Post successfully deleted!')
    else:
        flash("Post not found!")
    return redirect(url_for('index'))


# Route to edit a blog post by its ID
@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    post = blog.get_post(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Get updated form data
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        content = request.form.get('content', '').strip()

        errors = validate_post_form(title, author, content)

        if errors:
            for error in errors:
                flash(error)
            return redirect(url_for('edit', post_id=post_id))

        # Update the existing post{'title': new_title, 'content': new_content}
        if blog.update_post(post_id, {'author':author, 'title':title, 'content': content}):
            flash(f"Post with id {post_id} updated successfully!")
        else:
            flash("Error updating post. Please try again.")

        return redirect(url_for('index'))
    # Render the form for GET requests
    return render_template('edit.html', post=post)

@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    if blog.like_post(post_id):
        pass
    else:
        flash("Error liking post. Please try again.")
    # Likes the post, reloads the page and returns to the same post
    return redirect(url_for('index') + f"#post-{post_id}")

# Run the Flask application
if __name__ == '__main__':
    app.run()
