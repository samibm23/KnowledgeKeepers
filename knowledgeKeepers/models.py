from django.db import models

# Create your models here.
class TextInput(models.Model):
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)



from django.contrib.auth.models import User
from django.db import models

class Face(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    encoding = models.TextField(null=True, blank=True)

class Infos(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthday = models.DateField()
    parent_email = models.EmailField()
    parent_phone_number = models.CharField(max_length=15)
    grade = models.TextField(null=True,blank=True)
    mathcurrency = models.IntegerField(default=5)
    language = models.TextField(default="english",max_length=50)

class Role(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.TextField(max_length=255, default="Student")
    
    

class Avatar(models.Model):
    name = models.CharField(max_length=100)
    unique_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    selected = models.BooleanField(default=False)
    imageurl = models.TextField(max_length=250,default="")
    def __str__(self):
        return self.name
    

class MathProblemHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem_text = models.CharField(max_length=255)
    user_answer = models.CharField(max_length=255)
    real_answer = models.CharField(max_length=255)
    problem_id = models.IntegerField()
    result = models.CharField(max_length=255)
    numOfMistakes = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

