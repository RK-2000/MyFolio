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
    phone_no = models.CharField(max_length=10, blank=True, null=True)


class Link(models.Model):
    link_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=False, null=False)
    link = models.URLField(blank=False, null=False)


class UserSkills(models.Model):
    CHOICES = ((0, 'Low'), (1, 'Normal'), (2, 'High'),
               )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    expertise = models.IntegerField(default=0, choices=CHOICES)


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


class Interest(models.Model):
    interest_id = models.AutoField(primary_key=True)
    interest = models.CharField(max_length=50, blank=False, null=False)


class Certifications(models.Model):
    certificate_id = models.AutoField(primary_key=True)
    certificate_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    certificate_name = models.CharField(max_length=40, blank=False, null=False)
    certificate_auth_id = models.CharField(max_length=60, blank=False, null=False)
