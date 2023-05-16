from django.db import models


class Quest(models.Model):
    quest_name_ru = models.CharField(
        max_length=50, help_text="Enter the quest's name (ru)")
    quest_description_ru = models.TextField(
        help_text="Enter the quest's discription (ru)")
    quest_start_ru = models.TextField(
        help_text="Enter the quest's restrictons and start location (ru)")
    quest_name_en = models.CharField(
        max_length=50, help_text="Enter the quest's name (en)")
    quest_description_en = models.TextField(
        help_text="Enter the quest's discription (en)")
    quest_start_en = models.TextField(
        help_text="Enter the quest's restrictons and start location (en)")
    quest_image = models.ImageField(
        upload_to="uploads", help_text="Upload an image for the quest")
    quest_time = models.CharField(
        max_length=10, help_text="Enter estimate time to complete the "
                                 "quest (minutes)")

    def __str__(self):
        return self.quest_name_en


class Scene(models.Model):
    name = models.CharField(
        max_length=50, help_text="Enter the scene's name (ru)")
    panorama = models.ImageField(
        upload_to="uploads", help_text="Upload an panorama for the quest")
    quest = models.ForeignKey(
        Quest,
        on_delete=models.CASCADE,
        help_text="Select a quest for this scene",
    )

class PageParagraph(models.Model):
    number = models.IntegerField(
        help_text="Enter a parahraph's number (min is 0)")
    paragraph_ru = models.TextField(
        help_text="Enter the paragraph (ru)",
        blank=True,
    )
    paragraph_en = models.TextField(
        help_text="Enter the paragraph (en)",
        blank=True,
    )
    image = models.ImageField(
        upload_to="uploads", help_text="Upload the image for the "
                                       "paragraph (optional)", null=True, blank=True)
    image_description_en = models.TextField(
        help_text="image desctiption en",
        blank=True,
    )
    image_description_ru = models.TextField(
        help_text="image desctiption ru",
        blank=True,
    )
    page = models.ForeignKey(
        Scene,
        on_delete=models.CASCADE,
        help_text="Select a page for this Paragraph",
    )


class Points(models.Model):
    coord = models.IntegerField(
        help_text="Enter the coordinates")
    text = models.TextField(
        help_text="Text for the scene", blank=True)
    hint = models.TextField(
        help_text="Text for the hint scene", blank=True)
    answer = models.TextField(
        help_text="Text for the scene", blank=True)
    audio = models.FileField(
        upload_to="uploads", help_text="Upload the voice acting "
                                       "(ru, optional)", blank=True)
    quest_scene = models.ForeignKey(
        Scene,
        on_delete=models.CASCADE,
        help_text="Select a page for this answer",
        null=True,
    )

class Meta:
    ordering = ["number"]


def __str__(self):
    return str(self.page) + ", p " + str(self.number)


class PageAnswer(models.Model):
    page_answer_ru = models.CharField(
        max_length=30, help_text="Enter an answer for the page "
                                 "(ru, only lower case)")
    page_answer_en = models.CharField(
        max_length=30, help_text="Enter an answer for the page "
                                 "(en, only lower case)")
    quest_page = models.ForeignKey(
        Scene,
        on_delete=models.CASCADE,
        help_text="Select a page for this answer",
        null=True,
    )

    def __str__(self):
        return str(self.quest_page) + ", ans " + self.page_answer_en


class PageHint(models.Model):
    hint_text_ru = models.TextField(help_text="Enter a hint for the page (ru)")
    hint_text_en = models.TextField(help_text="Enter a hint for the page (en)")
    quest_page = models.ForeignKey(
        Scene,
        on_delete=models.CASCADE,
        help_text="Select a scene for this hint",
        null=True,
    )

    def __str__(self):
        return str(self.quest_page) + ", hint " + self.hint_text_en


class FeedBack(models.Model):
    q_id = models.IntegerField()
    user_name = models.CharField(max_length=30)
    convenience = models.IntegerField()
    complexity = models.IntegerField()
    text_quality = models.IntegerField()
    what_to_delete = models.TextField()
    what_to_add = models.TextField()
    did_quest_help = models.IntegerField()
    recommendation = models.IntegerField()
    why_such_ans = models.TextField()
    rate = models.IntegerField()

    def __str__(self):
        return self.user_name


class CorrectPageAnswer(models.Model):
    correct_page_answer_ru = models.CharField(
        max_length=30, help_text="Enter a full correct answer for the page "
                                 "(ru)")
    correct_page_answer_en = models.CharField(
        max_length=30, help_text="Enter a full correct answer for the page "
                                 "(en)")
    quest_page = models.ForeignKey(
        Scene,
        on_delete=models.CASCADE,
        help_text="Select a page for this answer",
        null=True,
    )

    def __str__(self):
        return str(self.quest_page) + ", ans " + self.correct_page_answer_en
