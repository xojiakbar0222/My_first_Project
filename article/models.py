from django.db import models
from django.urls import reverse

# Create your models here.
STATUS = (
    ('active', 'Active'),
    ('deactive', 'Deactive')
)

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Post_Mavzusi')
    
    status = models.CharField(max_length = 20, choices = STATUS, verbose_name='Holati', default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'
        ordering = ('-created_at',)
    
    def get_absolute_url(self):
        return reverse('article:catogories_list', args=[self.id,])


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_post', verbose_name = 'Post_Mavzusi')
    title = models.CharField(max_length=150, verbose_name='Sarlavha')
    subtitle = models.CharField(max_length=250, verbose_name = 'Sub_Matn', blank=True, null=True)
    body = models.TextField(verbose_name='Maqola')
    photo = models.ImageField(upload_to='posted_photos/%Y/%m/%d/', verbose_name='Rasm', blank=True, null=True)
    video = models.FileField(upload_to = 'posted_videos/%Y/%m/%d/', verbose_name='Video', blank=True, null=True)
    author = models.CharField(max_length=50, verbose_name='Mauallif')
    tag = models.CharField(max_length=25)
    views = models.PositiveIntegerField(default=1, verbose_name='Korishlar_soni')

    status = models.CharField(max_length = 20, choices = STATUS, verbose_name='Holati', default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Maqola'
        verbose_name_plural = 'Maqolalar'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article:detail', args=[self.id,])
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='izohlar')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Izoh'
        verbose_name_plural = 'Izohlar'

    def __str__(self) -> str:
        return f'{self.name} - {self.email}'




