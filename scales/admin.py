from django.contrib import admin

# Register your models here.
from .models import Question,Choice,Topic,Section,Computed,Record

# admin.site.register(Question)
# admin.site.register(Choice)
# admin.site.register(Topic)
# admin.site.register(Section)
admin.site.register(Computed)
# admin.site.register(Record)

class RecordAdmin(admin.ModelAdmin):
    list_display = ('question_id', "answer_text",'pub_date')

admin.site.register(Record, RecordAdmin)

class SectionInline(admin.StackedInline):
    model = Section
    extra = 3

class TopicAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['topic_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [SectionInline]
    list_display = ('topic_text', 'pub_date')

admin.site.register(Topic, TopicAdmin)

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 3

class SectionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['section_text'],'fields': ['body_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [QuestionInline]
    list_display = ('section_text', 'pub_date')

admin.site.register(Section,SectionAdmin)

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    def save(*args, **kwargs): 
        self.date = datetime.datetime.now() 
        super(Message, self).save(*args, **kwargs) 
    inlines = [ChoiceInline]
    list_display = ('question_text','was_published_recently')
    # list_filter = ['pub_date']# “过滤器”侧边栏
    search_fields = ['question_text']# 搜索功能

admin.site.register(Question, QuestionAdmin)