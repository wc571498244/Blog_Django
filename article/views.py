from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


from article.forms import WriteForm, CommentsForm
from article.models import Article, Tag, Comments
from user.models import UserProfile


def get_details_info():
    context = {}
    tags = Tag.objects.all()
    # 标签云
    tags_cloud = tags
    context['tags_cloud'] = tags_cloud
    # 文章分类
    tags = tags[:3]
    context["tags"] = tags
    # 点击排行
    click_rank = Article.objects.all().order_by("-click_num")[:15]
    context["click_rank"] = click_rank
    # 收藏排行
    love_rank = Article.objects.all().order_by("-love_num")[:15]
    context["love_rank"] = love_rank
    return context


# 文章详情
def details(request):
    context = {}
    if request.method == "GET":
        context.update(get_details_info())
        # 获取文章id
        a_id = request.GET.get("article_id", 1)
        # 查找id所对应的文章信息
        article_info = Article.objects.get(pk=a_id)
        article_info.click_num += 1
        article_info.save()
        context["article_info"] = article_info
        # 上一篇
        front_article = Article.objects.filter(date__gt=article_info.date).first()
        context['front_article'] = front_article
        # 下一篇
        next_article = Article.objects.filter(date__lt=article_info.date).last()
        context['next_article'] = next_article

        # 评论表单
        cform = CommentsForm()
        context['cform'] = cform

        # 评论列表
        comments = Comments.objects.filter(article=article_info.id).order_by("-date")
        # print(comments)
        context['comments'] = comments
    return render(request, "article/details.html", context=context)


# 文章列表
def article_list(request):
    context = {}
    context.update(get_details_info())
    tag_id = request.GET.get("tag_id")
    if tag_id:
        context["tag_id"] = int(tag_id)
    # 如果获取到tag_id就显示tag的所有文章
    if tag_id:
        tag = Tag.objects.get(pk=tag_id)
        context["tag"] = tag
        articles = Article.objects.filter(tags=tag).order_by("-date")
    else:
        articles = Article.objects.all().order_by("-date")
    # 分页
    context.update(get_pages_info(articles, 3, request))
    return render(request, "article/article_list.html", context=context)


def time_tree(request):
    context = {}
    articles = Article.objects.all().order_by("-date")
    context.update(get_pages_info(articles, 20, request))
    return render(request, 'article/time_tree.html', context=context)


# 获取分页信息
def get_pages_info(articles, num, request):
    context = {}
    # 分页
    paginator = Paginator(articles, num)  # 生成分页器，两个参数，一个被分页对象，一个是每页显示记录条数
    # print("count:", paginator.count)  # 数据总数(多少篇文章)
    # print("num_pages:", paginator.num_pages)  # 总页数
    # print("page_range:", paginator.paginator)  # 页码的列表（页码）

    # 获取当前页码
    current_page = int(request.GET.get("page", 1))
    context["current_page"] = current_page
    current_articles = paginator.get_page(current_page)  # 第一页的page对象
    context['current_articles'] = current_articles
    # 分页范围  (最多显示5页)
    if paginator.num_pages > 5:  # (如果大于5就分成若干个)
        if current_page - 2 < 1:  # 如果前面的页不够5
            page_range = range(1, 6)
        elif current_page + 2 > paginator.num_pages:  # 如果后面的不够5
            page_range = range(current_page - 2, paginator.num_pages + 1)
        else:
            page_range = range(current_page - 2, current_page + 3)
    else:  # 如果小于5 就显示全部
        page_range = paginator.page_range
    context["page_range"] = page_range
    return context


@login_required
# 写博客
def write_article(request):
    context = {}
    if request.method == "GET":
        # 富文本表单
        form = WriteForm()
        context["form"] = form
        # 获取所有的标签
        tags = Tag.objects.all()
        context["tags"] = tags
        return render(request, 'article/write_article.html', context=context)
    else:
        # 获取表单提交上来的数据
        title = request.POST["title"]
        desc = request.POST['desc']
        content = request.POST['content']
        img = request.FILES["img"]
        tags = request.POST.getlist('tags')  # 获取select中的多选
        userId = request.POST["userId"]
        # 查找用户id对应的用户对象
        user = UserProfile.objects.get(pk=userId)
        # 添加数据到article对象
        article = Article.objects.create(title=title, desc=desc, content=content, img=img, user=user)
        # 存many-to-many字段不能直接存，需要单独的拿出来 对象.属性.set(字段)
        article.tags.set(tags)
        article.save()
        context['article_id'] = article.id
        return render(request, 'article/write_success.html', context=context)


def send_comments(request):
    try:
        userId = request.GET.get("userId")
        articleId = request.GET.get("articleId")
        content = request.GET.get("content")
        user = UserProfile.objects.get(pk=userId)
        article = Article.objects.get(pk=articleId)
        comment = Comments.objects.create(content=content, user=user, article=article)
        json_data = {'status': 1}
    except:
        json_data = {'status': 0}
    return JsonResponse(json_data)
