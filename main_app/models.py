from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CHOICES = [('1', '2'),
           ('3', '4', '5')]


class Blog(models.Model):
    blog_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    author_fn = models.CharField(blank=False, null=False, max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True, null=True, upload_to='images/blog_images/')


class Skill(models.Model):
    skill_id = models.AutoField(primary_key=True)
    skill_name = models.CharField(max_length=40, blank=False, null=False)

    def __str__(self):
        return self.skill_name


class UserCompleteProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dob = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(blank=True, null=True, upload_to='images/profile_pictures/')
    about = models.TextField(blank=True, null=True)


class Link(models.Model):
    link_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=False, null=False)
    link = models.URLField(blank=False, null=False)


class UserSkills(models.Model):
    skill_user_id = models.AutoField(primary_key=True)
    CHOICES = (("1", 'Novice'), ('11', 'Moderate'), ('111', 'Proficient'), ('1111', 'Expert'),
               )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    expertise = models.CharField(default="1", max_length=4, choices=CHOICES)


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100)
    project_desc = models.TextField()
    project_link = models.URLField(blank=True, null=True)


class Education(models.Model):
    edu_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=50, blank=False, null=False)
    degree = models.CharField(max_length=50, blank=False, null=False)
    start_year = models.DateField(blank=False, null=False)
    end_year = models.DateField(blank=True, null=True)
    grade = models.CharField(max_length=10, blank=True, null=True)


class Documents(models.Model):
    document_id = models.AutoField(primary_key=True)
    document_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.FileField(blank=True, null=True, upload_to='images/documents/')
