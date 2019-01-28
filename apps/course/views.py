from django.shortcuts import render
from apps.cms.models import Course,CourseCategory
from .serializers import Courseserializers
from utils import restiful
from django.conf import settings
# Create your views here.
def course_list(request):
    courses = Course.objects.select_related('teacher').all()
    category = CourseCategory.objects.all()

    context = {
        'courses': courses,
        'category': category
    }
    return render(request, 'news/courselive.html', context=context)


def course_detail(request, course_id):
    return render(request,'news/course_detail.html')


def course_asny(request):
    category = int(request.GET["category"] or 0)
    # per_page_count = settings.COUNT_PER_PAGE
    if category != 0:
        categorys = CourseCategory.objects.get(pk=category)
        courses = Course.objects.filter(category=categorys)
    else:
        courses = Course.objects.all()
    course_data = Courseserializers(courses,many=True)
    print(course_data.data)
    return restiful.success(data=course_data.data)

