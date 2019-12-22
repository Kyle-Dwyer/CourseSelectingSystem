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
    if domain_and_record_db_datas is None:
        return {"error": "学（工）号或密码错误", "login": False, "Type": None}
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

    period = request.session.get("period", 0)
    request.session.clear()

    request.session["period"] = period

    if info.get("login") is True:
        if info.get("Type") == 0:
            request.session["Admin"] = id

        elif info.get("Type") == 1:
            request.session["teacher_id"] = id

        elif info.get("Type") == 2:
            request.session["student_id"] = id

    return JsonResponse(info)

