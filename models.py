from django.conf import settings
from django.db import models
from django.utils import timezone

from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation

class Post(models.Model, HitCountMixin):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to = "images/")
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
	post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
	author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	comment = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)

	def approve(self):
		self.approved_comment = True
		self.save()
