from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^index/', views.index,name='studentInfo'),
    url(r'^studentInfoManage/', views.showStudentInfoManage,name='studentInfoManage'),
    url(r'^saveInfo/', views.saveStudentInfo,name='saveStudentInfo'),
    url(r'^courseTable/', views.showCourseTable, name='courseTable'),
]