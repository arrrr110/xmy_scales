from django import template
from scales.models import Topic,Section,Question

register = template.Library()


# @template.inclusion_tag("index.html")
# def topic_tree(cate):
#     return {'topic':cate.categories.all()}

@register.filter(name="pick")
def pick(value,n):# 将question按照section的索引分离出来
    # print('&&&&',value.section_id)
    w_num = 1
    
    for e in value.keys():
        print(e[-1:])
        if e[-1:] == str(n):
            return value.pop(e)
        else:
            pass



@register.filter(name="xx")
def xx(value):
    return '%sxx' % value

# @register.filter(name="pick")
# def pick(value,n):# 将question按照section的索引分离出来
#     for e in value:
#         if e.section_id == n:
#             return e.question_text
#         else:
#             pass