# _*_ coding:utf-8 _*_
__author__ = '111'
__date__ = '2018/1/3 21:45'

from django.conf.urls import url
from .views import OrgView,AddAskView,OrgHomeView,OrgCourseView,OrgDescView,OrgTeacherView, AddFavView

urlpatterns = [

    url(r'^list/$',OrgView.as_view(), name='org-list'),
    url(r'^add_ask/$',AddAskView.as_view(),name='add_ask'),
    url(r'^home/(?P<org_id>\d+)/$',OrgHomeView.as_view(),name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$',OrgCourseView.as_view(),name='org_course'),
    url(r'^desc/(?P<org_id>\d+)/$',OrgDescView.as_view(),name='org_desc'),
    url(r'^teacher/(?P<org_id>\d+)/$',OrgTeacherView.as_view(),name='org_teacher'),
    #机构收藏
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),
]
