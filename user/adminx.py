import xadmin
from xadmin import views


class BaseSetting(object):
    enable_themes = True # 允许使用主题
    use_bootswatch = True


class GlobalSetting(object):
    site_title = "博客后台管理"
    site_footer = "WCC的博客后台管理"


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)

