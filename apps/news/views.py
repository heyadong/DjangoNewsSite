from django.shortcuts import render
from django.http import HttpResponse
from utils.captcha.captcha import Captcha
from utils import restiful
from io import BytesIO
from django.views.decorators.http import require_POST
from utils.smssdk.smssend import send_sms
import random
from apps.cms.models import Article, NewsTag, Banners
from django.core.cache import cache
from django.conf import settings
from apps.cms.serializers import ArticleSerialize
from .forms import CommentForms
from .models import Comments
from .serializers import Commentserialize
# Create your views here.


def index(request):
    tags = NewsTag.objects.all()
    end_page = settings.COUNT_PER_PAGE
    articles = Article.objects.select_related('author','tag').all().order_by('-pub_time')[0:end_page]
    banners = Banners.objects.all().order_by('-position')
    context = {
        "articles": articles,
        "tags": tags,
        "banners": banners
    }
    return render(request, 'news/index.html',context=context)


def newslist(request):
    #  djangorestframework 异步新新闻列表

    page = int(request.GET.get('page',1))
    print(page)
    start_count = page * settings.COUNT_PER_PAGE
    end_count = start_count + settings.COUNT_PER_PAGE
    category_id = int(request.GET.get('category',0))  # 新闻分类的id为0 是默认查找所有新闻分类
    if category_id != 0:
        tag = NewsTag.objects.get(pk=category_id)
        articles = Article.objects.filter(tag=tag)[start_count:end_count]
        articles_serialize = ArticleSerialize(articles, many=True)  # 使用djangorestframework序列化
    else:
        articles = Article.objects.all()[start_count:end_count]
        articles_serialize = ArticleSerialize(articles, many=True)

    return restiful.success(data=articles_serialize.data)

# 新闻详情页
def news_detail(request, news_id):
    # select_related 将外键关联的模型数据也提取出来减少查询次数。
    article = Article.objects.select_related('author','tag').get(pk=news_id)
    comments = Comments.objects.filter(article=article)
    context = {
        'article': article,
        'comments':comments
    }
    return render(request, 'news/news_detail.html',context=context)


# 新闻评论
@require_POST
def news_comment(request):
    form = CommentForms(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        content = data.get('content')
        news_id = int(data.get('article'))
        author = request.user  # 当前默认登陆用户
        article = Article.objects.get(pk=news_id)
        try:
            Comments.objects.create(content=content,author=author,article=article)
            return restiful.success()
        except:
            return restiful.paramserror(message="服务器内部错误，添加评论失败")
    else:
        return restiful.paramserror(data=form.get_errors())


# 评论列表：
def comment_list(request):
    # 每页显示评论数 per_page_count = 3
    news_id = int(request.GET.get('article'))
    per_page_count = 3
    article = Article.objects.get(pk=news_id)
    page = int(request.GET.get('page', 1))
    start = per_page_count * (page-1)
    end = start + per_page_count
    print(article)
    comments = Comments.objects.filter(article=article)[start:end]
    comments = Commentserialize(comments, many=True)
    return restiful.success(data=comments.data)


def search(request):
    return render(request, 'news/search.html')


def draw_example(request):
    text,image = Captcha.gene_code()
    out = BytesIO()
    image.save(out,'png') # 将对象保存到BytesIO中
    out.seek(0)   # 移动文件指针
    cache.set('image_text',text.lower())
    httpresponse = HttpResponse(content_type='image/png')
    httpresponse.write(out.read())
    httpresponse["Content-length"] = out.tell()
    return httpresponse


def sms_send(request):
    sms_code = random.randint(1000, 9999)
    cache.set('sms_code', sms_code, 60*5) # 存储验证码 并设置5分钟过期
    # params = {
    #     'code': sms_code
    # }
    # result = send_sms('17623008502',params)
    return HttpResponse("成功发送验证码："+str(sms_code))

