from django.contrib import admin
from quest.models import CorrectPageAnswer, FeedBack
from quest.models import PageAnswer, PageHint, Quest, QuestPage
from quest.models import PageParagraph

admin.site.register(Quest)
admin.site.register(QuestPage)
admin.site.register(PageAnswer)
admin.site.register(CorrectPageAnswer)
admin.site.register(PageHint)
admin.site.register(FeedBack)


@admin.register(PageParagraph)
class PageParagraphAdmin(admin.ModelAdmin):
    list_filter = ('page',)
