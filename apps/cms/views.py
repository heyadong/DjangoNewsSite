from django.shortcuts import render, reverse, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.views.decorators.http import require_POST
from django.views import View
from .models import NewsTag, Article,Banners
from .forms import TagForm, TagForm2, ArticleForm,BannerForm
from utils import restiful
from django.conf import settings
from django.core.paginator import Paginator
import os
User = get_user_model()


# def uplaodfile(file):
#     filename = os.path.join(settings.MEDIA_URL, file.name)
#     try:
#         with open(filename, 'wb') as file_obj:
#             for chunk in file.chunks():
#                 file_obj.write(chunk)
#     except Exception as e:
#         print(e)

#
# def uplaod(request):
#     form = BannerForm(request.POST,request.FILES)
#     if form.is_valid():
#         form.save()
#         return restiful.success()
#     else:
#         return restiful.paramserror(message=form.get_errors())


def cms_login(request):
    return render(request, 'CMS/cms_login.html')


def cms_index(request):
    return render(request, 'CMS/cms_index.html')


class Newslist(View):
    def get(self, request):
        per_page_count = 2
        tags = NewsTag.objects.all()
        articles = Article.objects.select_related('author', 'tag')
        page = int(request.GET.get('p','1') or 1)
        tag = int(request.GET.get('tag',0))
        start_time = request.GET.get('s_time')
        end_time = request.GET.get('e_time')
        title = request.GET.get('title','')
        author = request.GET.get('author','')
        if tag != 0:
            articles = articles.filter(tag__id=tag)
        if title:
            articles = articles.filter(title__icontains=title)
        if author:
            articles = articles.filter(author__username__icontains=author)
        paginator = Paginator(articles, per_page_count)
        page_obj = paginator.page(page)
        context_date = self.get_pagination_data(paginator=paginator,page_obj=page_obj)
        context = {
            'articles': articles,
            'page_obj': page_obj,
            'paginator': paginator,
            'tags': tags,
            'tag_id':tag
        }
        context.update(context_date)
        return render(request, 'CMS/cms_newsquery.html', context=context)

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        """
        通用分页算法
        :param paginator: 分页
        :param page_obj: 当前页
        :param around_count: 当前页码两边的页数
        :return:
        """
        current_page = page_obj.number  # 当前页码
        num_pages = paginator.num_pages  # 总页码
        left_has_more = False
        right_has_more = False
        left_pages = range(1,current_page)
        right_pages = range(current_page,num_pages+1)
        if current_page - around_count > 2:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)
        if current_page + around_count < num_pages - 1:
            right_has_more = True
            right_pages = range(current_page, current_page+around_count + 1)
        page_data = {
            'current_page': current_page,
            'num_pages': num_pages,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'left_pages': left_pages,
            'right_pages': right_pages,
        }
        return page_data

# 类视图
class CmsNews(View):
    def get(self, request):
        tags = NewsTag.objects.all()
        context = {
            "tags": tags
        }
        return render(request, 'CMS/cms_article.html', context=context)

    def post(self, request):
        form = ArticleForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            title = data.get('title')
            description = data.get('description')
            thumbnail = data.get('thumbnail')
            tag = data.get("tag")
            categoryTag = NewsTag.objects.get(pk=tag)
            content = data.get('content')
            # 登陆功能出翔bug 暂时指定发布作者
            # author = request.user
            author = User.object.get(pk='Bx9BnppGDx4gwqjwQ8rLvD')
            print(title, description, thumbnail, tag, content)
            try:
                Article.objects.create(title=title,
                                       thumbnail=thumbnail,
                                       description=description,
                                       tag=categoryTag,
                                       content=content,
                                       author=author)
                return restiful.success()
            except:
                return restiful.paramserror(message="参数错误")
        else:
            return restiful.paramserror(data=form.get_errors())




class NewsCategory(View):
    # 新闻分类添加
    def get(self, request):
        tags = NewsTag.objects.all()
        context = {
            'tags': tags
        }
        return render(request, 'CMS/cms_newstag.html', context=context)

    def post(self, request):
        form = TagForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data.get('tag')
            exist_tags = NewsTag.objects.filter(name=name)
            if exist_tags:
                return restiful.paramserror(message="标签已经存在")
            tag = NewsTag(name=name)
            tag.save()
            return redirect(reverse("cms:category"))
        else:
            return restiful.paramserror(message='参数错误')




def tag_delete(request, id):
    # 新闻分类删除
    if id:
        tag = NewsTag.objects.get(id=id)
        tag.delete()
        return restiful.success(message="删除标签成功")
    else:

        return restiful.paramserror(message="删除的标签不存在")


@require_POST
def tag_edit(request):
    # 新闻分类编辑
    form = TagForm2(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        tag_name = data.get('tag')
        tag_id = data.get('id')
        try:
            tag = NewsTag.objects.get(id=tag_id)
            tag.name = tag_name
            tag.save()
            return restiful.success()
        except:
            return restiful.paramserror("编辑的的标签不存在")


def banners(request):
    # 轮播图页面 （新增功能）
    if request.method == "POST":

        form = BannerForm(request.POST)
        if form.is_valid():
            data = form.data
            bannersimg = data.get('bannersimg')
            link_to = data.get('link_to')
            position = data.get('position')
            Banners.objects.create(bannersimg=bannersimg,link_to=link_to,position=position)
            return restiful.success(message="添加轮播图成功")
        else:
            return restiful.paramserror(data=form.get_errors())
    banners = Banners.objects.all()
    return render(request, 'CMS/cms_banners.html',context={'banners':banners})

@require_POST
def bannersdelete(request):
    banners_id = request.POST['banners_id']
    banner = Banners.objects.get(pk=banners_id)
    if banner:
        banner.delete()
        return restiful.success(message="删除轮播图成功")
    else:
        return restiful.paramserror(message="删除的轮播图不存在")


def bannersedit(request):
    banners_id = request.POST.get('banners_id')
    banner = Banners.objects.get(pk=banners_id)





@require_POST
def upload(request):
    """
  上传文件到本地
    """
    file = request.FILES.get('file')
    # try:
    with open(os.path.join(settings.MEDIA_ROOT,file.name),'wb') as file_obj:
        for chunk in file.chunks():
            file_obj.write(chunk)
    # file_url = request.SERVER_NAME+':'+request.SERVER_PORT+'/'+file.name
    file_url = 'http://' + request.get_host()+'/media/'+file.name
    return restiful.success(message="上传文件成功",data={'file_url': file_url,'file_name': file.name})
    # except:
    #     return restiful.paramserror(message="参数错误")


