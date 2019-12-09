from django.shortcuts import render
from django.db import connection


# Create your views here.
def get_stu_info(stu_id):
    if stu_id is None:
        return {'error': "no stu_id"}
    SQL_str = "select * from student where s_id = %s"
    cursor = connection.cursor()
    cursor.execute(SQL_str, [stu_id])
    domain_and_record_db_datas = cursor.fetchone()
    print(len(domain_and_record_db_datas))
    print(domain_and_record_db_datas)
    student_id = domain_and_record_db_datas[0]
    name = domain_and_record_db_datas[1]
    dept_name = domain_and_record_db_datas[2]
    phone_num = domain_and_record_db_datas[3]
    tot_cred = domain_and_record_db_datas[4]
    return {'s_id': student_id, 'name': name, 'dept_name': dept_name, 'phone_num': phone_num, 'tot_cred': tot_cred}


def index(request):
    stu_id = request.session.get('student_id')
    if stu_id is None:
        print("No stu_id")
        return render(request, 'student/studentInfo.html', {'error': "no stu_id"})
    print("debug", stu_id)
    info = get_stu_info(stu_id)
    return render(request, 'student/studentInfo.html', info)


def showCourseTable(request):
    return render(request, 'student/courseTable.html')
