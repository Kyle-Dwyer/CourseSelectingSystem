from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/', views.index),
    url(r'^teacherInfoManage/', views.showTeacherInfoMessage, name="teacherInfoManage"),
    url(r'^saveInfo/', views.saveTeacherInfoMessage, name="saveTeacherInfo"),
]
