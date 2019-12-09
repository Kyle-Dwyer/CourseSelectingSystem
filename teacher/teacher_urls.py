from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/', views.index,name="teacherInfo"),
    url(r'^teacherInfoManage/', views.showTeacherInfoMessage, name="teacherInfoManage"),
    url(r'^saveInfo/', views.saveTeacherInfoMessage, name="saveTeacherInfo"),

    url(r'^courseApply/', views.showCourseApply, name="teacherCourseApply"),
    url(r'^registerScore/', views.showRegisterScore, name="registerScore"),
]
