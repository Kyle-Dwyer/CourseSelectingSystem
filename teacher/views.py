import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection
from django.db import transaction


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
    info = get_tea_info(tea_id)
    return render(request, 'teacher/teacherInfo.html', info)


def showTeacherInfoMessage(request):
    return render(request, 'teacher/teacherInfoManage.html', get_tea_info(request.session.get('teacher_id')))


def saveTeacherInfoMessage(request):
    tea_id = request.session.get('teacher_id')
    if tea_id is None:
        print("No tea_id")
        return render(request, 'teacher/teacherInfo.html', {'error': "no tea_id"})
    phone_num = request.GET.get('phone_num')
    state = upadate_tea_info(tea_id, phone_num)
    print(state)
    return JsonResponse({"state": state})


def showCourseApply(request):
    return render(request, 'teacher/courseApply.html')


def showHandleApply(request):
    pageSize = 6
    page = int(request.GET.get('page', 1))

    tea_id = request.session.get('teacher_id')
    sql = "select course_id, sec_id, course_name, s_id, apply_reason, handle_reason from apply natural join main.section natural join teaches natural join course where i_id = %s and state = 0"
    cursor = connection.cursor()
    cursor.execute(sql, [tea_id])
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
            s_id = results[i][3]
            apply_reason = results[i][4]
            handle_reason = results[i][5]

            returnList.append(
                {'course_id': course_id + '.' + str(sec_id), 'course_name': course_name, 's_id': s_id,
                 'reason': apply_reason,
                 'handle_reason': handle_reason})

        return JsonResponse({'pageSize': pageSize, 'currentPage': page, 'totalNum': len(results), 'list': returnList})


def showHandledApply(request):
    pageSize = 6
    page = int(request.GET.get('page', 1))

    tea_id = request.session.get('teacher_id')
    sql = "select course_id, sec_id, course_name, s_id, apply_reason, handle_reason, state from apply natural join main.section natural join teaches natural join course where i_id = %s and state != 0"
    cursor = connection.cursor()
    cursor.execute(sql, [tea_id])
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
            s_id = results[i][3]
            apply_reason = results[i][4]
            handle_reason = results[i][5]
            state = int(results[i][6])
            if state == 0:
                state = "正在处理"
            elif state == 1:
                state = "申请成功"
            elif state == 2:
                state = "申请失败"
            elif state == 3:
                state = "已过期"

            returnList.append(
                {'course_id': course_id + '.' + str(sec_id), 'course_name': course_name, 's_id': s_id,
                 'reason': apply_reason,
                 'handle_reason': handle_reason, 'state': state})

        return JsonResponse({'pageSize': pageSize, 'currentPage': page, 'totalNum': len(results), 'list': returnList})


def handleApply(request):
    course_id = request.GET.get('course_id', ".")
    c_id = course_id.split(".")[0]
    sec_id = course_id.split(".")[1]
    period = request.session["period"]
    print(period)
    state = request.GET.get('state', 0)
    if period != 0:
        state = 3

    handle_reason = request.GET.get('handle_reason', "")
    s_id = request.GET.get('s_id', "")

    sql = "update apply set state = %s, handle_reason = %s where course_id = %s and sec_id = %s and s_id = %s"

    cursor = connection.cursor()
    cursor.execute(sql, [int(state), handle_reason, c_id, sec_id, s_id])

    return JsonResponse({"error": None, "handled": True})


def teacherCourse(request):
    return render(request, 'teacher/teacherCourse.html')


def showTeacherCourse(request):
    pageSize = 6
    page = int(request.GET.get('page', 1))

    tea_id = request.session.get('teacher_id')
    sql = "select course_id, sec_id, course_name, building, room_num, ctime_slot_id from main.section natural join teaches natural join course where i_id = %s"
    cursor = connection.cursor()
    cursor.execute(sql, [tea_id])
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
            building = results[i][3]
            room_num = results[i][4]
            ctime_slot_id = results[i][5]

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
                {'course_id': course_id + '.' + str(sec_id), 'course_name': course_name,
                 'place': building + '.' + str(room_num), 'ctime': ctime})

        return JsonResponse({'pageSize': pageSize, 'currentPage': page, 'totalNum': len(results), 'list': returnList})


def showCourseRoster(request):
    pageSize = 6
    page = int(request.GET.get('page', 1))

    course_id = request.GET.get('course_id', ".")
    if course_id is '.':
        return JsonResponse({'pageSize': pageSize, 'currentPage': page, 'totalNum': 0, 'list': []})

    c_id = course_id.split(".")[0]
    sec_id = course_id.split(".")[1]
    sql = "select s_id, student.name, dept_name, takes.credit from student natural join takes where course_id = %s and sec_id = %s and takes.dropped = 0"
    cursor = connection.cursor()
    cursor.execute(sql, [c_id, sec_id])
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
            grade = results[i][3]
            if grade is None or grade == "":
                grade = "成绩暂未公布"
            returnList.append(
                {'s_id': s_id, 'name': name, 'dept_name': dept_name, 'grade': grade})

        return JsonResponse({'pageSize': pageSize, 'currentPage': page, 'totalNum': len(results), 'list': returnList})


def showAddCourse(request):
    return render(request, 'teacher/addCourse.html')


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
            print(day)
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
    if int(limit) > result[0]:
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
            cursor.execute(sql, [c_id, sec_id, exam_type, e_day, etime_slot_id, building, room_num])

            # 插入teaches表
            sql = "insert into teaches (i_id, course_id, sec_id, `year`, semester) values (%s, %s, %s, 2019, 1)"
            cursor.execute(sql, [i_id, c_id, sec_id])
    except Exception:
        connection.connection.rollback()
        return {"error": "开课失败，请稍后再试！", "success": False}

    return {"error": None, "success": True}


def addCourse(request):
    i_id = request.session.get('teacher_id')
    # 读取数据
    course_id = request.GET.get('course_id', ".")
    c_id = course_id.split(".")[0]

    course_name = request.GET.get('course_name', "")
    dept_name = request.GET.get('dept_name', "")
    building = request.GET.get('building', "")
    room_num = request.GET.get('room_num', "")
    credit = request.GET.get('credit', "")
    limit = request.GET.get('limit', "")

    days = request.GET.getlist('days', "")
    start_times = request.GET.getlist('start_times', "")
    end_times = request.GET.getlist('end_times', "")

    print(days)
    print(start_times)
    print(end_times)

    exam_type = int(request.GET.get('type', 0))
    e_day = request.GET.get('e_day', "")
    e_start_time = request.GET.get('e_start_time', "")
    e_end_time = request.GET.get('e_end_time', "")

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
        sql = "select * from course where course_id = %s and course_name = %s and dept_name = %s and credits = %s"
        cursor.execute(sql, [c_id, course_name, dept_name, credit])

        # 开课院系、学分冲突，则开课失败，请求重新填写信息
        if cursor.fetchone() is None:
            return JsonResponse({"error": "开课失败，课程代码已被占用，课程名称、开课院系、学分等信息冲突！"})

        # 开课院系、学分不冲突，则进行进一步的冲突检查
        else:
            # 得到sec_id(该门课已开课的数目 + 1)
            sql = "select count(*) from section where course_id = %s"
            cursor.execute(sql, [c_id])
            sec_id = cursor.fetchone()[0] + 1

            return JsonResponse(
                insert_tables(i_id, c_id, sec_id, building, room_num, limit, ctime_slot_id, days, start_times,
                              end_times,
                              etime_slot_id, e_day, e_start_time, e_end_time, exam_type))

    # course表中不存在这门课，直接插入
    else:
        sql = "insert into course (course_id, course_name, credits, dept_name) values (%s, %s, %s, %s)"
        try:
            cursor.execute(sql, [c_id, course_name, credit, dept_name])
        except Exception:
            connection.connection.rollback()
            return {"error": "开课失败，请稍后再试！"}

        return JsonResponse(
            insert_tables(i_id, c_id, 1, building, room_num, limit, ctime_slot_id, days, start_times, end_times,
                          etime_slot_id, e_day, e_start_time, e_end_time, exam_type))


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    return False


def registerScore(request):
    course_id = request.GET.get('course_id', ".")
    c_id = course_id.split(".")[0]
    sec_id = course_id.split(".")[1]

    s_id = request.GET.get('s_id', "")
    grade = str(request.GET.get('grade', None))

    cursor = connection.cursor()
    period = request.session["period"]

    if period != 1:
        return JsonResponse({"error": "登分失败，不在登分期间！", "handled": False})

    if grade is not None:
        if not is_number(grade):
            return JsonResponse({"error": "登分失败，输入的分数不合法！", "handled": False})

    grade = float(grade)
    if grade > 100:
        return JsonResponse({"error": "登分失败，输入的分数超过了100分！", "handled": False})

    try:
        with transaction.atomic():
            # 更新总学分
            sql = "select takes.credit from takes where course_id = %s and sec_id = %s and s_id = %s"
            cursor.execute(sql, [c_id, int(sec_id), s_id])

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
        return JsonResponse({"error": "登分失败，请稍后重试！", "handled": False})
    return JsonResponse({"error": None, "handled": True})


def teacherLoadGrades(request):
    # 如果不在考试期间，不能进入该页面
    period = request.session.get("period", 0)

    print("period:%s" % period)
    if period != 1:
        return render(request, 'error.html', {"msg": "当前不在考试期间，无法进行登分操作！"})
    return render(request, 'teacher/loadGrades.html')


def register_excel_score(s_id, c_id, sec_id, year, semester, grade, i_id):
    cursor = connection.cursor()

    sql = "select i_id from teaches where course_id = %s and sec_id = %s and `year` = %s and semester = %s and i_id = %s"
    cursor.execute(sql, [c_id, int(sec_id), year, semester, i_id])
    result = cursor.fetchone()
    if result is None:
        return {"error": "登分失败，不是该教师开设的课程！", "handled": False}

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


def teacherLoadGradesExcel(request):
    if request.method == 'POST' and request.FILES.get('file'):

        filename = request.FILES['file']

        file = pd.read_csv(filename)

        file.fillna('无')

        cursor = connection.cursor()

        success_list = []
        fail_list = []

        i_id = request.session.get('teacher_id')
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

                        msg = register_excel_score(s_id, course_id, sec_id, year, semester, credit, i_id)
                        if msg["handled"] is False:
                            raise Exception(msg["error"])
                        else:
                            success_list.append(
                                {"line": i, "s_id": s_id, "course_id": course_id + '.' + str(sec_id), "year": year,
                                 "semester": semester, "credit": credit, "error": msg["error"]})
                    except Exception as e:
                        if str(e) == "'NoneType' object is not subscriptable":
                            e = "学生信息不存在！"
                        if str(e).find("invalid literal") != -1:
                            e = "输入信息不合法！"
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
