from django.db import models


class Post(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    Like_Count = models.IntegerField(default=0)
    def __str__(self):
        return self.title
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title