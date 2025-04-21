import json
import os


class BlogPost:
    def __init__(self, author, title, content, _id=None):
        self.author = author
        self.title = title
        self.content = content
        self._id = _id

    @classmethod
    def from_dict(cls, data):
        return cls(
            author=data.get('author'),
            title=data.get('title'),
            content=data.get('content'),
            _id=data.get('id')
        )

    def to_dict(self):
        return {
            'id': self._id,
            'title': self.title,
            'content': self.content,
            'author': self.author
        }

    def __str__(self):
        return f"{self.title} by {self.author}:\n{self.content}\n"

class BlogManager():
    def __init__(self, file_path):
        self.file_path = file_path

    def _load_posts(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def _save_posts(self, posts):
        with open(self.file_path, 'w') as f:
            json.dump(posts, f)

    def add_post(self, new_post):
        posts = self._load_posts()
        new_post._id = max((post['id'] for post in posts), default=0) + 1
        posts.append(new_post.to_dict())
        self._save_posts(posts)
        print("Post added successfully")

    def get_all_posts(self):
        return [BlogPost.from_dict(post) for post in self._load_posts()]

    def get_post(self, _id):
        posts = self._load_posts()
        for post in posts:
            if post['id'] == _id:
                return BlogPost.from_dict(post)
        print("Post not found")

    def update_post(self, _id, updated_data):
        posts = self._load_posts()
        for i, post in enumerate(posts):
            if post['id'] == int(_id):
                posts[i].update(updated_data.to_dict() if isinstance(updated_data, BlogPost) else updated_data)
                self._save_posts(posts)
                print("Post updated successfully")
                return True
        print("Post not found")
        return False

    def delete_post(self, _id):
        posts = self._load_posts()
        for i, post in enumerate(posts):
            if post['id'] == int(_id):
                del posts[i]
                self._save_posts(posts)
                print("Post deleted successfully")
                return True
        print("Post not found")
        return False

    def __str__(self):
        posts = self.get_all_posts()
        return "\n".join(str(post) for post in posts)

# Example usage
if __name__ == "__main__":
    blog = BlogManager()
    post = BlogPost("John", "Hello World", "This is my first blog post")
    blog.add_post(post)
    blog.update_post(2, {'title': 'new title', 'content': 'bla bla bla'})
    blog.delete_post(3)
    print(blog)


