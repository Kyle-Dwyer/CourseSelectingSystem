from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection

info = None


# Create your views here.
def get_tea_info(tea_id):
    if tea_id is None:
        return {'error': "no tea_id"}
    SQL_str = "select * from instructor where i_id = %s"
    cursor = connection.cursor()
    cursor.execute(SQL_str, [tea_id])
    domain_and_record_db_datas = cursor.fetchone()
    print(len(domain_and_record_db_datas))
    print(domain_and_record_db_datas)
    teacher_id = domain_and_record_db_datas[0]
    name = domain_and_record_db_datas[1]
    dept_name = domain_and_record_db_datas[2]
    phone_num = domain_and_record_db_datas[3]
    salary = domain_and_record_db_datas[4]
    return {'i_id': teacher_id, 'name': name, 'dept_name': dept_name, 'phone_num': phone_num, 'salary': salary}


def upadate_tea_info(tea_id, phone_num):
    if tea_id is None:
        return {'error': "no tea_id"}
    SQL_str = "update instructor set phone_num = %s where i_id = %s"
    cursor = connection.cursor()
    try:
        cursor.execute(SQL_str, [phone_num, tea_id])
    except Exception:
        connection.connection.rollback()
        return False
    return True


def index(request):
    tea_id = request.session.get('teacher_id')
    if tea_id is None:
        print("No tea_id")
        return render(request, 'teacher/teacherInfo.html', {'error': "no tea_id"})
    global info
    info = get_tea_info(tea_id)
    return render(request, 'teacher/teacherInfo.html', info)


def showTeacherInfoMessage(request):
    return render(request, 'teacher/teacherInfoManage.html', info)


def saveTeacherInfoMessage(request):
    tea_id = request.session.get('teacher_id')
    if tea_id is None:
        print("No tea_id")
        return render(request, 'teacher/teacherInfo.html', {'error': "no tea_id"})
    phone_num = request.GET.get('phone_num')
    state = upadate_tea_info(tea_id, phone_num)
    print(state)
    return JsonResponse({"state": state})
