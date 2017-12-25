# _*_ coding:utf-8 _*_
__author__ = '111'
__date__ = '2017/12/23 16:57'

import xadmin
from .models import UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']  # 列表显示
    search_fields = ['name', 'mobile', 'course_name']  # 搜索
    list_filter = ['name', 'mobile', 'course_name', 'add_time']  # 筛选


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']  # 列表显示
    search_fields = ['user', 'course', 'comments']  # 搜索
    list_filter = ['user', 'course', 'comments', 'add_time']  # 筛选


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']  # 列表显示
    search_fields = ['user', 'fav_id', 'fav_type']  # 搜索
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']  # 筛选


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']  # 列表显示
    search_fields = ['user', 'message', 'has_read']  # 搜索
    list_filter = ['user', 'message', 'has_read', 'add_time']  # 筛选


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']  # 列表显示
    search_fields = ['user', 'course']  # 搜索
    list_filter = ['user', 'course', 'add_time']  # 筛选


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
