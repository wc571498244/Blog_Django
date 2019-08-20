import xadmin
from article.models import Article, Tag


class ArticleAdmin(object):
    list_display = ['title', 'date', 'click_num', 'love_num', 'user']  # 显示的列表
    search_fields = ['title', 'date']  # 可查找的字段
    list_filter = ['date', 'user']  # 过滤
    list_editable = ['click_num', "love_num"]  # 设置默认可编辑字段，在列表里就可以编辑
    list_per_page = 10  # 每页显示的数量
    ordering = ('-date',)  # 设置默认排序字段，负号表示降序排序(按照时间降序)


class TagAdmin(object):
    list_display = ["name"]
    search_fields = ['name']
    list_filter = ['name']


xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Tag, TagAdmin)
