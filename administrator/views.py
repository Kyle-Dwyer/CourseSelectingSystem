from django.db import transaction, connection
from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd


# Create your views here.
def index(request):
    return render(request, 'administrator/administrator.html')


def loadStudent(request):
    return render(request, 'administrator/loadStudent.html')


def studentExcel(request):
    if request.method == 'POST' and request.FILES.get('file'):

        filename = request.FILES['file']

        file = pd.read_csv(filename)

        cursor = connection.cursor()

        success_list = []
        fail_list = []

        rollback = False

        try:
            with transaction.atomic():
                for i in range(file.shape[0]):
                    s_id = str(file.iloc[i, 0])
                    password = str(file.iloc[i, 1])
                    name = str(file.iloc[i, 2])
                    dept_name = str(file.iloc[i, 3])
                    phone_num = str(file.iloc[i, 4])
                    tot_cred = str((file.iloc[i, 5]))

                    try:
                        tot_cred = int(tot_cred)
                        sql = "select * from account where user_id = %s"
                        cursor.execute(sql, [s_id])

                        result = cursor.fetchone()
                        if result is None:
                            sql = "insert into account (user_id, password, role) values (%s, %s, 2)"
                            cursor.execute(sql, [s_id, password])
                        sql = "insert into student (s_id, name, dept_name, phone_num, tot_cred) values (%s, %s, %s, %s, %s)"
                        cursor.execute(sql, [s_id, name, dept_name, phone_num, tot_cred])
                        success_list.append(
                            {'s_id': s_id, 'name': name, 'dept_name': dept_name, 'phone_num': phone_num,
                             'tot_cred': tot_cred})
                    except Exception as e:
                        if str(e) == "UNIQUE constraint failed: student.s_id":
                            e = "学生已存在！"
                        if str(e).find("invalid literal") != -1:
                            e = "输入信息不合法！"
                        connection.connection.rollback()
                        fail_list.append(
                            {'s_id': s_id, 'name': name, 'dept_name': dept_name, 'phone_num': phone_num,
                             'tot_cred': tot_cred,
                             "fail_reason": str(e)})
                        rollback = True
                        continue
                if rollback:
                    raise Exception

        except Exception as e:
            print(e)

        return JsonResponse(
            {"code": 0, "msg": "学生信息导入数据库成功！", "success_num": len(success_list), "fail_num": len(fail_list),
             "fail_list": fail_list})

    else:
        return JsonResponse(
            {"code": 0, "msg": "导入失败！", "success_num": None, "fail_num": None, "fail_list": None})


def studentList(request):
    return render(request, 'administrator/studentList.html')


def showStudentList(request):
    pageSize = 6
    page = int(request.GET.get('page', 1))

    sql = "select * from student"
    cursor = connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()

    returnList = []

    if len(results) is 0:
        return JsonResponse({'pageSize': pageSize, 'currentPage': page, 'totalNum': 0, 'list': []})
    else:
        fromIndex = (page - 1) * pageSize
        toIndex = min(len(results), page * pageSize)

        for i in range(fromIndex, toIndex):
            s_id = results[i][0]
            name = results[i][1]
            dept_name = results[i][2]
            phone_num = results[i][3]
            tot_cred = results[i][4]

            returnList.append(
                {'s_id': s_id, 'name': name, 'dept_name': dept_name,
                 'phone_num': phone_num,
                 'tot_cred': tot_cred})

        return JsonResponse({'pageSize': pageSize, 'currentPage': page, 'totalNum': len(results), 'list': returnList})


def loadInstructor(request):
    return render(request, 'administrator/loadInstructor.html')


def instructorExcel(request):
    if request.method == 'POST' and request.FILES.get('file'):

        filename = request.FILES['file']

        file = pd.read_csv(filename)

        cursor = connection.cursor()

        success_list = []
        fail_list = []

        rollback = False

        try:
            with transaction.atomic():
                for i in range(file.shape[0]):
                    i_id = str(file.iloc[i, 0])
                    password = str(file.iloc[i, 1])
                    name = str(file.iloc[i, 2])
                    dept_name = str(file.iloc[i, 3])
                    phone_num = str(file.iloc[i, 4])
                    salary = str((file.iloc[i, 5]))

                    try:
                        salary = int(salary)
                        sql = "select * from account where user_id = %s"
                        cursor.execute(sql, [i_id])

                        result = cursor.fetchone()
                        if result is None:
                            sql = "insert into account (user_id, password, role) values (%s, %s, 1)"
                            cursor.execute(sql, [i_id, password])
                        sql = "insert into instructor (i_id, name, dept_name, phone_num, salary) values (%s, %s, %s, %s, %s)"
                        cursor.execute(sql, [i_id, name, dept_name, phone_num, salary])
                        success_list.append(
                            {'i_id': i_id, 'name': name, 'dept_name': dept_name, 'phone_num': phone_num,
                             'salary': salary})
                    except Exception as e:
                        if str(e).find("UNIQUE constraint failed") != -1:
                            e = "教师已存在！"
                        if str(e).find("invalid literal") != -1:
                            e = "输入信息不合法！"
                        connection.connection.rollback()
                        fail_list.append(
                            {'i_id': i_id, 'name': name, 'dept_name': dept_name, 'phone_num': phone_num,
                             'salary': salary,
                             "fail_reason": str(e)})
                        rollback = True
                        continue
                if rollback:
                    raise Exception

        except Exception as e:
            print(e)

        return JsonResponse(
            {"code": 0, "msg": "教师信息导入数据库成功！", "success_num": len(success_list), "fail_num": len(fail_list),
             "fail_list": fail_list})

    else:
        return JsonResponse(
            {"code": 0, "msg": "导入失败！", "success_num": None, "fail_num": None, "fail_list": None})


def instructorList(request):
    return render(request, 'administrator/instructorList.html')


def showInstructorList(request):
    pageSize = 6
    page = int(request.GET.get('page', 1))

    sql = "select * from instructor"
    cursor = connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()

    returnList = []

    if len(results) is 0:
        return JsonResponse({'pageSize': pageSize, 'currentPage': page, 'totalNum': 0, 'list': []})
    else:
        fromIndex = (page - 1) * pageSize
        toIndex = min(len(results), page * pageSize)

        for i in range(fromIndex, toIndex):
            i_id = results[i][0]
            name = results[i][1]
            dept_name = results[i][2]
            phone_num = results[i][3]
            salary = results[i][4]

            returnList.append(
                {'i_id': i_id, 'name': name, 'dept_name': dept_name,
                 'phone_num': phone_num,
                 'salary': salary})

        return JsonResponse({'pageSize': pageSize, 'currentPage': page, 'totalNum': len(results), 'list': returnList})


def no_conflict(start1, end1, start2, end2):
    if str(start1) > str(end2) or str(end1) < str(start2):
        return True
    else:
        return False


def check_ctime(i_id, days, start_times, end_times):
    sql = "select ctime_slot.day, start_time, end_time from teaches natural join section natural join ctime_slot where i_id = %s"
    cursor = connection.cursor()
    cursor.execute(sql, [i_id])
    result = cursor.fetchall()

    # 该教师没有教课
    if len(result) == 0:
        return {"error": None, "success": True}
    else:
        for i in range(len(days)):  # 要开的课每行判断
            day = days[i]
            # print(day)
            if day in [result[a][0] for a in range(len(result))]:  # 如果有新的day才判断这一行，否则跳过
                start1 = start_times[i]
                end1 = end_times[i]
                # print(1, day, start1, end1)
                for day2, start2, end2 in result[:]:  # 抽出该day已选课程所有的时间段
                    # print(2, day2, start2, end2)
                    if day2 == day and not no_conflict(start1, end1, start2, end2):
                        return {"error": "开课失败，与本人已开设课程的上课时间冲突", "success": False}

        return {"error": None, "success": True}


def check_ctime_and_place(days, start_times, end_times, building, room_num):
    sql = "select ctime_slot.day, start_time, end_time from main.section natural join ctime_slot where building = %s and room_num = %s"
    cursor = connection.cursor()
    cursor.execute(sql, [building, room_num])
    result = cursor.fetchall()

    if len(result) == 0:
        return {"error": None, "success": True}
    else:
        for i in range(len(days)):  # 要开的课每行判断
            day = days[i]

            if day in [result[a][0] for a in range(len(result))]:  # 如果有新的day才判断这一行，否则跳过
                start1 = start_times[i]
                end1 = end_times[i]
                # print(1, day, start1, end1)
                for day2, start2, end2 in result[:]:  # 抽出该day已选课程所有的时间段
                    # print(2, day2, start2, end2)
                    if day2 == day and not no_conflict(start1, end1, start2, end2):
                        return {"error": "开课失败，同一时间同一地点已经有其它的课！", "success": False}

        return {"error": None, "success": True}


def check_etime_and_place(e_day, e_start_time, e_end_time, building, room_num):
    sql = "select exam.day, start_time, end_time from exam natural join etime_slot where building = %s and room_num = %s and type = 0"
    cursor = connection.cursor()
    cursor.execute(sql, [building, room_num])
    result = cursor.fetchall()

    if len(result) == 0:
        return {"error": None, "success": True}
    else:
        if e_day in [result[a][0] for a in range(len(result))]:  # 如果有新的day才判断这一行，否则跳过
            # print(1, day, start1, end1)
            for day, start, end in result[:]:  # 抽出该day已选课程所有的时间段
                # print(2, day2, start2, end2)
                if e_day == day and not no_conflict(e_start_time, e_end_time, start, end):
                    return {"error": "开课失败，同一考试时间、同一地点有其它课程的考试！", "success": False}

        return {"error": None, "success": True}


def check_limit_and_capacity(limit, building, room_num):
    sql = "select capacity from classroom where building = %s and room_num = %s"
    cursor = connection.cursor()
    cursor.execute(sql, [building, room_num])
    result = cursor.fetchone()
    if limit > result[0]:
        return {"error": "开课失败，选课人数上限大于教室人数上限！", "success": False}
    else:
        return {"error": None, "success": True}


def insert_tables(i_id, c_id, sec_id, building, room_num, limit, ctime_slot_id, days, start_times, end_times,
                  etime_slot_id,
                  e_day, e_start_time, e_end_time, exam_type):
    cursor = connection.cursor()
    # 0. 初步检查：
    # 0.1. 检查时间段是否开始时间小于结束时间：
    for i in range(len(days)):
        if start_times[i] > end_times[i]:
            return {"error": "开课失败，输入的上课时间段不合法！", "success": False}

    if e_start_time > e_end_time:
        return {"error": "开课失败，输入的考试时间段不合法！", "success": False}

    # 0.2. 检查上课教室信息是否合法（即检查是否是classroom表中的值）
    sql = "select * from classroom where building = %s and room_num = %s"
    cursor.execute(sql, [building, room_num])

    if cursor.fetchone() is None:
        return {"error": "开课失败，输入的上课地点不合法！", "success": False}

    # 1. 检查该教师是否在冲突的时间同时上课
    message = check_ctime(i_id, days, start_times, end_times)
    if message.get("success") is False:
        return message

    # 2. 检查要开的这门课是否和其他开课的上课时间、地点同时冲突
    message = check_ctime_and_place(days, start_times, end_times, building, room_num)
    if message.get("success") is False:
        return message

    # 3. 检查要开的这门课是否和其他开课的考试时间、地点同时冲突
    if exam_type is 0:
        message = check_etime_and_place(e_day, e_start_time, e_end_time, building, room_num)
        if message.get("success") is False:
            return message

    # 4. 检查人数上限是否超过教室上限
    message = check_limit_and_capacity(limit, building, room_num)
    if message.get("success") is False:
        return message
    # 没有任何冲突，可以增加开课！
    # 插入section表

    try:
        with transaction.atomic():
            # 插入section表
            sql = "insert into main.section (course_id, sec_id, `year`, semester, building, room_num, ctime_slot_id, `limit`) values (%s, %s, 2019, 1, %s, %s, %s, 5)"
            cursor.execute(sql, [c_id, sec_id, building, room_num, ctime_slot_id])

            # 插入ctime_slot表
            sql = "insert into ctime_slot (ctime_slot_id, `day`, start_time, end_time) values (%s, %s, %s, %s)"
            for i in range(len(days)):
                day_i = days[i]
                start_time_i = start_times[i]
                end_time_i = end_times[i]
                cursor.execute(sql, [ctime_slot_id, day_i, start_time_i, end_time_i])

            # 插入etime_slot表
            sql = "insert into etime_slot (etime_slot_id, start_time, end_time) values (%s, %s, %s)"
            cursor.execute(sql, [etime_slot_id, e_start_time, e_end_time])

            # 插入exam表
            sql = "insert into exam (course_id, sec_id, `year`, semester, `type`, `day`, etime_slot_id, building, room_num) values (%s, %s, 2019, 1, %s, %s, %s, %s, %s)"
            # print([c_id, sec_id, exam_type, e_day, etime_slot_id, building, room_num])
            cursor.execute(sql, [c_id, sec_id, exam_type, e_day, etime_slot_id, building, room_num])

            # 插入teaches表
            sql = "insert into teaches (i_id, course_id, sec_id, `year`, semester) values (%s, %s, %s, 2019, 1)"
            cursor.execute(sql, [i_id, c_id, sec_id])
    except Exception:
        connection.connection.rollback()
        return {"error": "开课失败，请稍后再试！", "success": False}

    return {"error": None, "success": True}


def addCourse(request, i_id, c_id, course_name, dept_name, building, room_num, credit, limit, days, start_times,
              end_times,
              exam_type, e_day, e_start_time, e_end_time):
    cursor = connection.cursor()

    # 得到ctime_slot_id（section中的条目数 + 1）
    sql = "select count(*) from section"
    cursor.execute(sql)
    ctime_slot_id = cursor.fetchone()[0] + 1

    # 得到etime_slot_id（section中的条目数 + 1）
    sql = "select count(*) from exam"
    cursor.execute(sql)
    etime_slot_id = cursor.fetchone()[0] + 1

    # 首先检查course表中有没有这个课（根据course_id查找）
    sql = "select * from course where course_id = %s"

    cursor.execute(sql, [c_id])
    if cursor.fetchone() is not None:
        # course表中有这个课，检查输入的其他相关信息（开课院系、学分等是否有冲突）
        sql = "select * from course where course_id = %s and course_name = %s and credits = %s and dept_name = %s"
        cursor.execute(sql, [c_id, course_name, int(credit), dept_name])

        # 开课院系、学分冲突，则开课失败，请求重新填写信息
        a = cursor.fetchone()
        # print("debug1", a, [c_id, course_name, dept_name, credit])
        if a is None:
            # print("debug2")
            return {"error": "开课失败，课程代码已被占用，课程名称、开课院系、学分等信息冲突！", "success": False}

        # 开课院系、学分不冲突，则进行进一步的冲突检查
        else:
            # print("debug3")
            # 得到sec_id(该门课已开课的数目 + 1)
            sql = "select count(*) from section where course_id = %s"
            cursor.execute(sql, [c_id])
            sec_id = cursor.fetchone()[0] + 1

            return insert_tables(i_id, c_id, sec_id, building, room_num, limit, ctime_slot_id, days, start_times,
                                 end_times,
                                 etime_slot_id, e_day, e_start_time, e_end_time, exam_type)

    # course表中不存在这门课，直接插入,"success":False
    else:
        sql = "insert into course (course_id, course_name, credits, dept_name) values (%s, %s, %s, %s)"
        try:
            cursor.execute(sql, [c_id, course_name, credit, dept_name])
        except Exception:
            connection.connection.rollback()
            return {"error": "开课失败，请稍后再试！", "success": False}

        return insert_tables(i_id, c_id, 1, building, room_num, limit, ctime_slot_id, days, start_times, end_times,
                             etime_slot_id, e_day, e_start_time, e_end_time, exam_type)


def loadSection(request):
    return render(request, 'administrator/loadSection.html')


def sectionExcel(request):
    if request.method == 'POST' and request.FILES.get('file'):

        filename = request.FILES['file']

        file = pd.read_csv(filename)

        file.fillna('无')

        success_list = []
        fail_list = []

        rollback = False
        try:
            with transaction.atomic():
                for i in range(file.shape[0]):
                    try:
                        course_id = file.iloc[i, 0]
                        sec_id = file.iloc[i, 1]
                        year = int(file.iloc[i, 2])
                        semester = int(file.iloc[i, 3])
                        building = file.iloc[i, 4]
                        room_num = str(file.iloc[i, 5])
                        limit = int(file.iloc[i, 6])
                        e_day = file.iloc[i, 7]
                        e_start_time = file.iloc[i, 8]
                        e_end_time = file.iloc[i, 9]
                        i_id = file.iloc[i, 10]
                        type = int(file.iloc[i, 11])
                        course_name = file.iloc[i, 12]
                        credit = int(file.iloc[i, 13])
                        dept_name = file.iloc[i, 14]
                        c_day = file.iloc[i, 15]
                        c_start_time = file.iloc[i, 16]
                        c_end_time = file.iloc[i, 17]

                        c_days = c_day.strip("|").split("|")
                        c_start_times = c_start_time.strip("|").split("|")
                        c_end_times = c_end_time.strip("|").split("|")
                        msg = addCourse(request, i_id, course_id, course_name, dept_name, building, room_num, credit,
                                        limit,
                                        c_days, c_start_times,
                                        c_end_times,
                                        type, e_day, e_start_time, e_end_time)
                        if msg["success"] is False:
                            fail_list.append(
                                {"line": i, "course_id": course_id, "year": year, "semester": semester, "i_id": i_id,
                                 "error": msg["error"]})
                            raise ValueError(msg["error"])
                        else:
                            success_list.append(
                                {"line": i, "course_id": course_id, "year": year, "semester": semester, "i_id": i_id})
                    except ValueError as e:
                        rollback = True
                        continue
                    except Exception as e:
                        fail_list.append(
                            {"line": i, "course_id": course_id, "year": year, "semester": semester, "i_id": i_id,
                             "error": str(e)})
                        print(i, e)
                        rollback = True
                        continue
                if rollback:
                    raise Exception
        except Exception as e:
            print(e)

        return JsonResponse(
            {"code": 0, "msg": "开课信息导入数据库完成！", "success_num": len(success_list), "fail_num": len(fail_list),
             "fail_list": fail_list})

    return JsonResponse(
        {"code": 0, "msg": "开课信息导入数据失败！", "success_num": None, "fail_num": None,
         "fail_list": None})


def sectionList(request):
    return render(request, 'administrator/sectionList.html')


def showSectionList(request):
    pageSize = 6
    page = int(request.GET.get('page', 1))

    sql = "select course_id, sec_id, course_name, `year`, semester, building, room_num, `limit`, ctime_slot_id,credits,dept_name,i_id from `section` natural join course natural join teaches"
    cursor = connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()

    returnList = []

    if len(results) is 0:
        return JsonResponse({'pageSize': pageSize, 'currentPage': page, 'totalNum': 0, 'list': []})
    else:
        fromIndex = (page - 1) * pageSize
        toIndex = min(len(results), page * pageSize)

        for i in range(fromIndex, toIndex):
            course_id = results[i][0]
            sec_id = results[i][1]
            course_name = results[i][2]
            year = results[i][3]
            semester = results[i][4]
            building = results[i][5]
            room_num = results[i][6]
            limit = results[i][7]
            ctime_slot_id = int(results[i][8])
            credit = int(results[i][9])
            dept_name = results[i][10]
            i_id = results[i][11]
            sql = "select `day`, start_time, end_time from ctime_slot where ctime_slot_id = %s"
            cursor.execute(sql, [ctime_slot_id])
            result2 = cursor.fetchall()

            ctime = ""
            for j in range(len(result2)):
                day = result2[j][0]
                start_time = result2[j][1]
                end_time = result2[j][2]
                ctime += day + " " + str(start_time) + "-" + str(end_time) + ";"
            returnList.append(
                {'course_id': course_id + '.' + str(sec_id), 'course_name': course_name, 'year': year,
                 'semester': semester, "building": building, "room_num": room_num, "limit": limit,
                 'ctime': ctime, "credit": credit, "dept_name": dept_name, "i_id": i_id})

        return JsonResponse({'pageSize': pageSize, 'currentPage': page, 'totalNum': len(results), 'list': returnList})


def deleteSection(request):
    period = request.session.get("period", 0)

    if period != 0:
        return JsonResponse({"error": "删除课程失败，当前不在选课期间！"})

    course_id = request.GET.get('course_id', ".")
    c_id = course_id.split(".")[0]
    sec_id = course_id.split(".")[1]

    year = request.GET.get('year', "")
    semester = request.GET.get('semester', "")

    cursor = connection.cursor()

    sql = "select ctime_slot_id from `section` where course_id = %s and sec_id = %s and year = %s and semester = %s"
    cursor.execute(sql, [c_id, sec_id, year, semester])
    result = cursor.fetchone()
    ctime_slot_id = result[0]

    sql = "select etime_slot_id from exam where course_id = %s and sec_id = %s and year = %s and semester = %s"
    cursor.execute(sql, [c_id, sec_id, year, semester])
    result = cursor.fetchone()
    etime_slot_id = result[0]

    try:
        with transaction.atomic():
            sql = "delete from `section` where course_id = %s and sec_id = %s and year = %s and semester = %s"
            cursor.execute(sql, [c_id, sec_id, year, semester])

            sql = "delete from ctime_slot where ctime_slot_id = %s"
            cursor.execute(sql, [ctime_slot_id])

            sql = "delete from etime_slot where etime_slot_id = %s"
            cursor.execute(sql, [etime_slot_id])
    except Exception:
        connection.connection.rollback()
        return JsonResponse({"error": "删除课程失败，请稍后再试！"})

    return JsonResponse({"error": None})


def examList(request):
    return render(request, 'administrator/examList.html')


def showExamList(request):
    pageSize = 6
    page = int(request.GET.get('page', 1))

    sql = "select course_id, sec_id, course_name, `year`, semester, building, room_num, `type`, etime_slot_id, credits, `day` from `section` natural join course natural join exam"
    cursor = connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()

    returnList = []

    if len(results) is 0:
        return JsonResponse({'pageSize': pageSize, 'currentPage': page, 'totalNum': 0, 'list': []})
    else:
        fromIndex = (page - 1) * pageSize
        toIndex = min(len(results), page * pageSize)

        for i in range(fromIndex, toIndex):
            course_id = results[i][0]
            sec_id = results[i][1]
            course_name = results[i][2]
            year = results[i][3]
            semester = results[i][4]
            building = results[i][5]
            room_num = results[i][6]
            type = int(results[i][7])
            if type == 0:
                type = "考试"
            else:
                type = "论文"
            etime_slot_id = int(results[i][8])
            credit = int(results[i][9])
            day = results[i][10]
            sql = "select start_time, end_time from etime_slot where etime_slot_id = %s"
            cursor.execute(sql, [etime_slot_id])
            result2 = cursor.fetchone()

            etime = ""

            start_time = result2[0]
            end_time = result2[1]
            etime += (day + " " + str(start_time) + "-" + str(end_time))
            returnList.append(
                {'course_id': course_id + '.' + str(sec_id), 'course_name': course_name, 'year': year,
                 'semester': semester, "building": building, "room_num": room_num, "type": type,
                 'etime': etime, "credit": credit})

        return JsonResponse({'pageSize': pageSize, 'currentPage': page, 'totalNum': len(results), 'list': returnList})


def loadGrades(request):
    # 如果不在考试期间，不能进入该页面
    period = request.session.get("period", 0)

    print("period:%s" % period)
    if period != 1:
        return render(request, 'error.html', {"msg": "当前不在考试期间，无法进行登分操作！"})
    return render(request, 'administrator/loadGrades.html')


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    return False


def register_score(s_id, c_id, sec_id, year, semester, grade):
    cursor = connection.cursor()

    if grade is not None:
        if not is_number(grade):
            return {"error": "登分失败，输入的分数不合法！", "handled": False}

    grade = float(grade)
    if grade > 100:
        return {"error": "登分失败，输入的分数超过100分！", "handled": False}

    if grade < 0:
        return {"error": "登分失败，输入的分数小于0分！", "handled": False}
    try:
        with transaction.atomic():
            # 更新总学分
            sql = "select takes.credit from takes where course_id = %s and sec_id = %s and `year` = %s and semester = %s and s_id = %s"
            cursor.execute(sql, [c_id, int(sec_id), year, semester, s_id])

            result = cursor.fetchone()

            # 如果这门课之前的成绩为None，那么要同时更新一下总学分
            if result[0] is None:
                sql = "select credits from course where course_id = %s"
                cursor.execute(sql, [c_id])

                result = cursor.fetchone()

                credit = result[0]

                sql = "update student set tot_cred = tot_cred + %s where s_id = %s"

                cursor.execute(sql, [credit, s_id])

            # 否则，只更新分数
            sql = "update takes set `credit` = %s where course_id = %s and sec_id = %s and s_id = %s"
            cursor.execute(sql, [grade, c_id, int(sec_id), s_id])
    except Exception:
        raise
        connection.connection.rollback()
        return {"error": "登分失败，请稍后重试！", "handled": False}
    return {"error": None, "handled": True}


def gradesExcel(request):
    if request.method == 'POST' and request.FILES.get('file'):

        filename = request.FILES['file']

        file = pd.read_csv(filename)

        file.fillna('无')

        cursor = connection.cursor()

        success_list = []
        fail_list = []

        rollback = False
        try:
            with transaction.atomic():
                for i in range(file.shape[0]):
                    s_id = str(file.iloc[i, 0])
                    course_id = str(file.iloc[i, 1])
                    sec_id = str(file.iloc[i, 2])
                    year = str(file.iloc[i, 3])
                    semester = str(file.iloc[i, 4])
                    credit = str(file.iloc[i, 5])
                    try:
                        sec_id = int(sec_id)
                        year = int(year)
                        semester = int(semester)
                        credit = int(credit)

                        msg = register_score(s_id, course_id, sec_id, year, semester, credit)
                        if msg["handled"] is False:
                            raise Exception(msg["error"])
                        else:
                            success_list.append(
                                {"line": i, "s_id": s_id, "course_id": course_id + '.' + str(sec_id), "year": year,
                                 "semester": semester, "credit": credit, "error": msg["error"]})
                    except Exception as e:
                        if str(e).find("'NoneType'") != -1:
                            e = "请检查学生，课程信息是否合法"
                        fail_list.append(
                            {"line": i, "s_id": s_id, "course_id": course_id + '.' + str(sec_id), "year": year,
                             "semester": semester, "credit": credit, "error": str(e)})
                        rollback = True
                        continue
                if rollback:
                    raise Exception
        except Exception as e:
            print(e)

        return JsonResponse(
            {"code": 0, "msg": "分数信息导入数据库完成！", "success_num": len(success_list), "fail_num": len(fail_list),
             "fail_list": fail_list})

    return JsonResponse(
        {"code": 0, "msg": "分数信息导入数据失败！", "success_num": None, "fail_num": None,
         "fail_list": None})


def periodPage(request):
    period = request.session.get("period", 0)

    return render(request, 'administrator/modifyPeriod.html', {"period": period})


def changePeriod(request):
    period = request.GET.get("period", 0)
    if period == "true":
        period = 0
    else:
        period = 1
    request.session["period"] = period
    return JsonResponse({})
