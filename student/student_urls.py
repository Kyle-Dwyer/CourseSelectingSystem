from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/', views.index, name='studentInfo'),
    url(r'^studentInfoManage/', views.showStudentInfoManage, name='studentInfoManage'),
    url(r'^saveInfo/', views.saveStudentInfo, name='saveStudentInfo'),

    url(r'^courseTable/', views.showCourseTable, name='courseTable'),

    url(r'^courseApply/', views.showCourseApply, name='studentCourseApply'),
    url(r'^applyCourse/', views.applyCourse, name='applyCourse'),
    url(r'^showAppliedCourse/', views.showAppliedCourse, name='showAppliedCourse'),

    url(r'^courseManage/', views.showCourseManage, name='courseManage'),
    url(r'^showCourse/', views.showCourse, name='showCourse'),
    url(r'^selectCourse/', views.selectCourse, name='selectCourse'),
    url(r'^showSelectedCourse/', views.showSelectedCourse, name='showSelectedCourse'),
    url(r'^dejectCourse/', views.dejectCourse, name='dejectCourse'),

    url(r'^transcript/', views.transcript, name='transcript'),
    url(r'^showTranscript/', views.showTranscript, name='showTranscript'),

    url(r'^studentExamList/', views.studentExamList, name='studentExamList'),
    url(r'^showStudentExamList/', views.showStudentExamList, name='showStudentExamList'),
]
