from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import Question,Choice,Topic,Section,Computed,Record
from django.core.paginator import Paginator
# 这里需要把Topic,Section,Question,Choice都取出来，进行相应的排列
"""
第一部分：大节标题
	• 甲（n）
		○ Choice 1
			§ 0
			§ 1
		○ Choice 2
		○ ……
		○ Choice n
	• 乙
	• 丙
	• 丁
第二部分：
	• 甲
	• 乙

要无限细分才可以，形成一个多级列表
"""

def index(request):
    topic_1 = Topic.objects.get(id = 1)
    topic_2 = Topic.objects.get(id = 2)
    section_1 = Section.objects.filter(topic = 1)
    section_2 = Section.objects.filter(topic = 2)

    latest_question_list = Question.objects.all()
    question_1 = Question.objects.filter(section = 1)
    question_2 = Question.objects.filter(section = 2)
    print(question_2)
    # print(type(latest_question_list.get(section == 1)))

    # 建立一个大字典
    question_dict = {}
    w_num = 1
    
    while w_num <= 5:
        question_dict['q_list'+str(w_num)] = Question.objects.filter(section = w_num)
        w_num += 1
        
    print(question_dict)



    sum_score = 0
    question_id_list = []
    for e in Record.objects.all():
        # print("@@@@@",e.question_score)
        sum_score += e.question_score
        question_id_list.append(e.question_id)
    

    question_num = list(set(question_id_list))
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'scales/index.html', locals())

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    print("*"*10)

    return render(request, 'scales/detail.html', {
        'question': question,
        })

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # 提交并进入下一页
    question_list = Question.objects.all()
    paginator = Paginator(question_list,1) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    print(page_obj.has_previous)
    if question.id < question_list.count():
        page_next = question_id+1
        print("#####",page_next)
    else:
        # 这里是超范围导致页面错误，先放着
        pass
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'scales/detail.html', {
            'question': question,
            'error_message': "你必须做出一个选择",
        })
    else:
        record = Record(
            user_id = 0, 
            question_id = question_id, 
            question_score = selected_choice.score_int,
            answer_text = selected_choice.choice_text,
            )
        record.save()
        print('已记录数据----------',record)
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('scales:detail', args=(page_next,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'scales/results.html', {'question': question})