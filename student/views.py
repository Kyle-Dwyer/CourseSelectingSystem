from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'student/studentInfo.html')


def showCourseTable(request):
    return render(request, 'student/courseTable.html')
