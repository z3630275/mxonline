from django.shortcuts import render
from django.views.generic import View

from .models import CourseOrg,CityDict

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self,request):
        #课程机构
        all_orgs = CourseOrg.objects.all()

        #城市
        all_citys = CityDict.objects.all()
        #分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs,5, request=request)
        orgs = p.page(page)
        # 课程机构数量
        org_nums = all_orgs.count()
        return render(request,'org-list.html',{
            'all_orgs':orgs,
            'all_citys':all_citys,
            'org_nums':org_nums,

        })