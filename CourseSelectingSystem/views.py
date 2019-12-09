from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection


def _login(id, pwd):
    if id is None or pwd is None:
        return {"error": "学（工）号或密码不能为空", "login": False, "Type": None}
    SQL_str = "select password,role from account where user_id = %s"
    cursor = connection.cursor()
    cursor.execute(SQL_str, [id])
    domain_and_record_db_datas = cursor.fetchone()
    if pwd == domain_and_record_db_datas[0]:
        return {"error": None, "login": True, "Type": domain_and_record_db_datas[1]}
    else:
        return {"error": "学（工）号或密码错误", "login": False, "Type": None}


def login_page(request):
    return render(request, "./login.html")


def login(request):
    id = request.POST.get("id")
    pwd = request.POST.get("password")
    info = _login(id, pwd)
    if info.get("login") == True:
        if info.get("Type") == 0:
            request.session["Admin"] = id
            return render(request, "administrator/administrator.html")
        elif info.get("Type") == 1:
            request.session["teacher_id"] = id
            return render(request, "student/studentInfo.html")
        elif info.get("Type") == 2:
            request.session["teacher_id"] = id
            return render(request, "teacher/teacherInfo.html")
        else:
            return render(request, "./error.html", {"error": "Hacker!"})
    else:
        return JsonResponse({"error": info.get("error")})
