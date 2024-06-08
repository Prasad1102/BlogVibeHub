from django.db import models
import uuid
from django.contrib.auth.models import User

class BaseModel(models.Model):
  id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    abstract = True

class Follow(models.Model):
  follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
  following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

  class Meta:
    unique_together = (('follower', 'following'),)

class Blog(BaseModel):
  title = models.CharField(max_length=200)
  content = models.TextField()
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
  blog_image = models.ImageField(upload_to = "public/static/", default="/")
  like_count = models.IntegerField(default=0)

  def __str__(self):
    return self.title

  class Meta:
    ordering = ['-created_at']

class Comment(BaseModel):
  blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
  comment = models.CharField(max_length=800)

  def __str__(self):
    return f'Comment by {self.user.username} on {self.blog.title}'
