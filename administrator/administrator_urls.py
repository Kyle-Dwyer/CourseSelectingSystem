from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/', views.index),

    url(r'^loadStudent/', views.loadStudent, name="loadStudent"),
    url(r'^studentExcel/', views.studentExcel, name="studentExcel"),

    url(r'^studentList/', views.studentList, name="studentList"),
    url(r'^showStudentList/', views.showStudentList, name="showStudentList"),

    url(r'^loadInstructor/', views.loadInstructor, name="loadInstructor"),
    url(r'^instructorExcel/', views.instructorExcel, name="instructorExcel"),

    url(r'^instructorList/', views.instructorList, name="instructorList"),
    url(r'^showInstructorList/', views.showInstructorList, name="showInstructorList"),

    url(r'^sectionList/', views.sectionList, name="sectionList"),
    url(r'^showSectionList/', views.showSectionList, name="showSectionList"),
    url(r'^deleteSection/', views.deleteSection, name="deleteSection"),

    url(r'^loadSection/', views.loadSection, name="loadSection"),
    url(r'^sectionExcel/', views.sectionExcel, name="sectionExcel"),

    url(r'^loadGrades/', views.loadGrades, name="loadGrades"),
    url(r'^gradesExcel/', views.gradesExcel, name="gradesExcel"),

    url(r'^examList/', views.examList, name="examList"),
    url(r'^showExamList/', views.showExamList, name="showExamList"),

    url(r'^periodPage/', views.periodPage, name="periodPage"),
    url(r'^changePeriod/', views.changePeriod, name="changePeriod"),
]
