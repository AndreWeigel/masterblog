import json
import os


class BlogPost:
    """Represents a blog post"""
    def __init__(self, author, title, content, id=None, likes=0):
        self.author = author
        self.title = title
        self.content = content
        self.id = id
        self.likes = likes

    @classmethod
    def from_dict(cls, data):
        """Create a BlogPost instance from a dictionary"""
        return cls(
            author=data.get('author'),
            title=data.get('title'),
            content=data.get('content'),
            id=data.get('id'),
            likes = data.get('likes')
        )

    def to_dict(self):
        """Convert the BlogPost instance to a dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'likes': self.likes
        }

    def __str__(self):
        """String representation of the BlogPost instance"""
        return f"{self.title} by {self.author}:\n{self.content}\n"

class BlogManager():
    """Manages blog posts"""
    def __init__(self, file_path):
        self.file_path = file_path

    def _load_posts(self):
        """Load posts from the JSON file"""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def _save_posts(self, posts):
        """Save posts to the JSON file"""
        with open(self.file_path, 'w') as f:
            json.dump(posts, f)

    def add_post(self, new_post):
        """Add a new post to the blog"""
        try:
            posts = self._load_posts()
            new_post.id = max((post['id'] for post in posts), default=0) + 1
            posts.append(new_post.to_dict())
            self._save_posts(posts)
            print("Post added successfully")
            return True
        except Exception as e:
            print(f"Error adding post: {e}")
            return False

    def get_all_posts(self):
        """Get all posts from the blog"""
        return [BlogPost.from_dict(post) for post in self._load_posts()]

    def get_post(self, id):
        """Get a post by ID"""
        posts = self._load_posts()
        for post in posts:
            if post['id'] == id:
                return BlogPost.from_dict(post)
        print("Post not found")

    def update_post(self, id, updated_data):
        """Update a post by ID"""
        posts = self._load_posts()
        for i, post in enumerate(posts):
            if post['id'] == int(id):
                posts[i].update(updated_data.to_dict() if isinstance(updated_data, BlogPost) else updated_data)
                self._save_posts(posts)
                print("Post updated successfully")
                return True
        print("Post not found")
        return False

    def delete_post(self, id):
        """Delete a post by ID"""
        posts = self._load_posts()
        for i, post in enumerate(posts):
            if post['id'] == int(id):
                del posts[i]
                self._save_posts(posts)
                print("Post deleted successfully")
                return True
        print("Post not found")
        return False

    def like_post(self, id):
        """Increment the like count of a post by ID"""
        posts = self._load_posts()
        for post in posts:
            if post['id'] == int(id):
                post['likes'] = post['likes'] + 1
                self._save_posts(posts)
                print("Post liked successfully")
                return True
        print("Post not found")
        return False

    def __str__(self):
        """String representation of the BlogManager instance"""
        posts = self.get_all_posts()
        return "\n".join(str(post) for post in posts)

# Example usage
if __name__ == "__main__":
    blog = BlogManager("blog_posts.json")  # Specify a JSON file to persist blog data

    # Add a new post
    new_post = BlogPost("Alice", "A Day in the Park", "Today I went to the park and it was lovely.")
    blog.add_post(new_post)

    # Update the post with ID 1
    blog.update_post(1, {'title': 'A Sunny Day in the Park', 'content': 'It was warm and the birds were singing.'})

    # Delete the post with ID 1
    blog.delete_post(1)

    # Print all blog posts
    print(blog)
