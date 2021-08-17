from django.db import models
import django.utils.timezone as timezone
from django.contrib import admin
import datetime
# Create your models here.

# 大节标题
class Topic(models.Model):
    topic_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published',default = timezone.now)
    def __str__(self):
        return self.topic_text

# 小节标题
class Section(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    section_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published',default = timezone.now)
    body_text = models.TextField()
    def __str__(self):
        return self.section_text

# 具体问题
class Question(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published',default = timezone.now)
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    def __str__(self):
        return self.question_text

# 具体选项
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published',editable=False,default = timezone.now) 
    # 设为False,这个字段将不会出现在admin或者其他ModelForm，他们也会跳过模型验证，默认是True
    score_int = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

# 计算结果
class Computed(models.Model):
    sum_score = models.IntegerField(default=0)
    computed_text = models.TextField()
    pub_date = models.DateTimeField('date published',default = timezone.now)
    def __str__(self):
        return self.computed_text

# 回答记录
class Record(models.Model):
    user_id = models.IntegerField(default=0)
    question_id = models.IntegerField()
    question_score = models.IntegerField()
    answer_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published',default = timezone.now)
    def __str__(self):
        return self.answer_text
