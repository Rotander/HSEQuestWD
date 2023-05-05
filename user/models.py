from django.db import models
from quest.models import Quest, PageHint
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    pts = models.IntegerField(default=0)
    used_hints = models.IntegerField(default=0)
    full_name = models.CharField(max_length=50, blank=True)
    university = models.CharField(max_length=50, blank=True)
    ed_year = models.CharField(max_length=50, blank=True)
    faculty = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.username


class Game(models.Model):
    profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="Profile of user who play the game",
    )
    quest = models.ForeignKey(
        Quest,
        on_delete=models.CASCADE,
        help_text="Playes quest",
    )
    last_page = models.IntegerField()
    bought_hints = models.ManyToManyField(
        PageHint,
        blank=True
    )

    def __str__(self):
        return str(self.profile) + "'s playing " + str(self.quest)


class Present(models.Model):
    present_name_ru = models.CharField(
        max_length=50, help_text="Enter the present's name (ru)")
    present_description_ru = models.TextField(
        help_text="Enter the present's discription (ru)")
    present_name_en = models.CharField(
        max_length=50, help_text="Enter the present's name (en)")
    present_description_en = models.TextField(
        help_text="Enter the present's discription (en)")
    present_image = models.ImageField(
        upload_to="uploads", help_text="Upload an image of the present")
    present_cost = models.IntegerField(default=0)

    def __str__(self):
        return self.present_name_en


class ErrorReport(models.Model):
    error_report = models.TextField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Playes quest",
    )

    def __str__(self):
        return str(self.user) + '\' reporting'
