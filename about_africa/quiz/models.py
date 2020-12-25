from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    country = models.CharField(max_length=35)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name}'

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Quiz(models.Model):

    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete = models.PROTECT)
    region = models.CharField(max_length= 50)
    description = models.TextField(null=True, blank = True)
    creation_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("quiz-detail", kwargs={"pk": self.pk})
    

class Question(models.Model):
    prompt = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.PROTECT)
    answer_a = models.CharField(max_length=200)
    answer_b = models.CharField(max_length=200)
    answer_c = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1, choices=[['A', 'A'], ['B', 'B'], ['C', 'C']])

    def __str__(self):
        return self.prompt

class QuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.PROTECT)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    score = models.PositiveIntegerField()
    quiz_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.quiz.title + " - " + self.user_profile.user.username
