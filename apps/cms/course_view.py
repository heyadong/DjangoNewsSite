from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_http_methods
from django.views import View
from .forms import CourseForm,CourseCategoryForm
from .models import Course,CourseTeacher,CourseCategory
from utils import restiful
from django.db.models import Count

class CourseView(View):
    def get(self, request):
        teachers = CourseTeacher.objects.all()
        categorys = CourseCategory.objects.all()
        print(categorys)
        context = {
            'teachers': teachers,
            'categorys': categorys
        }
        return render(request, 'CMS/cms_course.html',context=context)

    def post(self, request):
        form = CourseForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            title = data.get('title')
            category_id = int(data.get('category'))
            teacher_id = int(data.get('teacher'))
            link = data.get('link')
            times = data.get('times')
            cover = data.get('cover')
            price = data.get('price')
            absract = data.get("abstract")
            teacher = CourseTeacher.objects.get(pk=teacher_id)
            category = CourseCategory.objects.get(pk=category_id)
            try:
                Course.objects.create(title=title,
                                      category=category,
                                      teacher=teacher,
                                      link=link,
                                      times=times,
                                      cover=cover,
                                      price=price,
                                      abstract=absract)
                return restiful.success(message="成功添加文章")
            except Exception as e:
                return restiful.paramserror(message=e)
        else:
            return restiful.paramserror(data=form.get_errors())


# 课程删除
def course_delete(request):
    course_id = request.POST.get('course_id')
    try:
        course = Course.objects.get(pk=course_id)
        course.delete()
        return restiful.success(message="成功删除电影")
    except:
        return restiful.paramserror(message="要删除的文章不存在")


# 课程展示页
class CourseList(View):
    def get(self, request):
        courses_list = Course.objects.select_related('teacher','category').all()
        print(courses_list)
        context = {
            'courses_list':courses_list,
        }
        return render(request,'CMS/course_list.html',context=context)

    def post(self,request):
        pass


class TeacherAdd(View):
    def get(self, request):
        return render(request,"CMS/course_teacher.html")
    def post(self,request):
        pass


class CourseTag(View):
    # 课程分类添加
    def get(self, request):
        # 分类查询课程数量
        # '<QuerySet [{'category': 'Python', 'course_count': 6}, {'category': 'Java', 'course_count': 0}]>
        category_count = CourseCategory.objects.annotate(
            course_count=Count('course')
        ).values('id',
                 'category',
                 'course_count')
        context = {
            'tags': category_count
        }
        return render(request, 'CMS/course_category.html', context=context)

    def post(self, request):
        form = CourseCategoryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            category = data.get('category')
            print(category)
            exist_tags = CourseCategory.objects.filter(category=category)
            if exist_tags:
                return restiful.paramserror(message="标签已经存在")
            tag = CourseCategory(category=category)
            tag.save()
            return redirect(reverse("cms:course_category"))
        else:
            return restiful.paramserror(message='参数错误',data=form.get_errors())


def coursecategory_edit(request):
    category_id = request.POST['category_id']
    tag_name = request.POST['name']
    print(tag_name)
    category = CourseCategory.objects.get(pk=category_id)
    if category:
        category.category = tag_name
        category.save()
        return restiful.success()
    else:
        return restiful.paramserror(message="更改的课程分类不存在")


def coursecategory_del(request):
    category_id = request.POST['category_id']
    course_category = CourseCategory.objects.get(pk=category_id)
    if course_category:
        course_category.delete()
        return restiful.success()
    else:
        return restiful.paramserror(message="删除的分类不存在")



