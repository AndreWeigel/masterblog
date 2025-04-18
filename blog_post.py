import json
import os

BLOG_POSTS_FILE = "blog_posts.json"

class BlogPost():
    def __init__(self, author, title, content):
        self.author = author
        self.title = title
        self.content = content
        self._id = None

    def save(self):
        blog_posts = []
        if os.path.exists(BLOG_POSTS_FILE):
            with open(BLOG_POSTS_FILE, "r") as file:
                try:
                    blog_posts = json.load(file)
                except json.JSONDecodeError:
                    blog_posts = []
            if blog_posts:
                last_id = max(post['id'] for post in blog_posts)
                self._id = last_id + 1
            else:
                self._id = 1
        else:
            self._id = 1

        post = {
            'id': self._id,
            'title': self.title,
            'content': self.content,
            'author': self.author

            }
        blog_posts.append(post)

        with open(BLOG_POSTS_FILE, "w") as file:
            json.dump(blog_posts, file)

    def __str__(self):
        return f"""{self.title} by {self.author}:\n{self.content}
                """

if __name__ == "__main__":
    post = BlogPost("John", "Hello World", "This is my first blog post")
    post.save()
    print(post)

