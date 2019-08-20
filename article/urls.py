from django.urls import path

from article.views import *

app_name = "article"

urlpatterns = [
    path("details/", details, name="details"),
    path("article_list/", article_list, name="article_list"),
    path("time_tree/", time_tree, name="time_tree"),  # 时间轴
    path("write_article", write_article, name="write_article"),
    path("send_comments", send_comments, name="send_comments"),

]
