from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/', views.index, name="teacherInfo"),

    url(r'^teacherInfoManage/', views.showTeacherInfoMessage, name="teacherInfoManage"),
    url(r'^saveInfo/', views.saveTeacherInfoMessage, name="saveTeacherInfo"),

    url(r'^courseApply/', views.showCourseApply, name="teacherCourseApply"),
    url(r'^showHandleApply/', views.showHandleApply, name="showHandleApply"),
    url(r'^showHandledApply/', views.showHandledApply, name="showHandledApply"),
    url(r'^handleApply/', views.handleApply, name="handleApply"),

    url(r'^teacherCourse/', views.teacherCourse, name="teacherCourse"),
    url(r'^showTeacherCourse/', views.showTeacherCourse, name="showTeacherCourse"),
    url(r'^showCourseRoster/', views.showCourseRoster, name="showCourseRoster"),

    url(r'^showAddCourse/', views.showAddCourse, name="showAddCourse"),
    url(r'^addCourse/', views.addCourse, name="addCourse"),

    url(r'^registerScore/', views.registerScore, name="registerScore"),

    url(r'^teacherLoadGrades/', views.teacherLoadGrades, name="teacherLoadGrades"),
    url(r'^teacherLoadGradesExcel/', views.teacherLoadGradesExcel, name="teacherLoadGradesExcel"),
]
