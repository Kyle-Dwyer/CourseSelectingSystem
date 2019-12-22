from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt


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


def showStudentInfoManage(request):
    return render(request, 'student/studentInfoManage.html', get_stu_info(request.session.get('student_id')))


def saveStudentInfo(request):
    stu_id = request.session.get('student_id')
    phone_num = request.GET.get("phone_num")
    sql = "update student set phone_num = %s where s_id = %s"
    cursor = connection.cursor()
    cursor.execute(sql, [phone_num, stu_id])
    return HttpResponse("更新信息成功")


def showCourseTable(request):
    return render(request, 'student/courseTable.html')


def showCourseApply(request):
    # 如果不在选课期间，不能进入该页面
    period = request.session.get("period", 0)

    print("period:%s" % period)
    if period != 0:
        return render(request, 'error.html', {"msg": "当前不在选课期间，无法进行选课申请！"})
    return render(request, 'student/courseApply.html')


def showCourseManage(request):
    # 如果不在选课期间，不能进入该页面
    period = request.session.get("period", 0)

    print("period:%s" % period)
    if period != 0:
        return render(request, 'error.html', {"msg": "当前不在选课期间，无法进行选退课操作！"})
    return render(request, 'student/courseManage.html')


def showCourse(request):
    course_id = request.GET.get('course_id', "")
    course_name = request.GET.get("course_name", "")
    page = int(request.GET.get('page', 1))
    pageSize = 6

    # print(course_id)
    # print(course_name)
    sql = "select course_id, sec_id, course_name, building, room_num, ctime_slot_id from course natural join `section` where course_id like %s and course_name like %s"
    cursor = connection.cursor()
    cursor.execute(sql, ['%' + course_id + '%', '%' + course_name + '%'])
    results = cursor.fetchall()

    returnList = []

    fromIndex = (page - 1) * pageSize
    toIndex = min(len(results), page * pageSize)
    for i in range(fromIndex, toIndex):
        result = results[i]

        ctime_slot_id = result[5]

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
            {'course_id': result[0] + '.' + str(result[1]), 'course_name': result[2], 'place': result[3] + "." + result[4],
             'ctime': ctime})

    # print(returnList)
    return JsonResponse({'pageSize': pageSize, 'currentPage': page, 'totalNum': len(results), 'list': returnList})


def no_conflict(start1, end1, start2, end2):
    if start1 > end2 or end1 < start2:
        return True
    else:
        return False


def _selectCourse(s_id, c_id, sec_id):
    error_none = {"error": "选课失败，该课程不存在", "selected": False}

    cursor = connection.cursor()
    # 插入还是更新
    check_sql = "select dropped from takes where s_id = %s and course_id = %s and sec_id = %s"
    cursor.execute(check_sql, [s_id, c_id, sec_id])
    drop = cursor.fetchone()
    insert = True
    if drop is not None:
        if drop[0] == 0:
            return {"error": "选课失败，该课程已在课表中", "selected": False}
        elif drop[0] == 1:
            insert = False
    # 人数限制
    select_limit_sql = "select `limit` from `section` where  course_id = %s and sec_id = %s"
    cursor.execute(select_limit_sql, [c_id, sec_id])
    result = cursor.fetchone()
    if result is None:
        return error_none
    else:
        limit = result[0]
    select_num_sql = "select count(*) from takes where course_id = %s and sec_id = %s and dropped = 0"
    cursor.execute(select_num_sql, [c_id, sec_id])
    result = cursor.fetchone()
    if result is None:
        return error_none
    else:
        num = result[0]
    if num >= limit:
        return {"error": "选课失败，人数已达上限", "selected": False}
    # 课程冲突
    selct_time_sql = "select * from ctime_slot where  ctime_slot_id = (select ctime_slot_id from `section` where course_id = %s and sec_id = %s)"
    cursor.execute(selct_time_sql, [c_id, sec_id])
    course_time = cursor.fetchall()
    # print(course_time)
    if course_time is None:
        return error_none
    select_selectedcourse_sql = "select * from ctime_slot where  ctime_slot_id in (select ctime_slot_id from `section` where (course_id,sec_id) in (select course_id,sec_id from takes where s_id = %s and dropped = 0))"
    cursor.execute(select_selectedcourse_sql, [s_id])
    selected_course_time = cursor.fetchall()
    # print(selected_course_time)
    if len(selected_course_time) != 0:
        for i in range(len(course_time)):  # 要选课程每行判断
            day = course_time[i][1]
            if day in [selected_course_time[a][1] for a in range(len(selected_course_time))]:  # 如果有新的day才判断这一行，否则跳过
                start1 = course_time[i][2]
                end1 = course_time[i][3]
                # print(1, day, start1, end1)
                for _, day2, start2, end2 in selected_course_time[:]:  # 抽出该day已选课程所有的时间段
                    # print(2, day2, start2, end2)
                    if day2 == day and not no_conflict(start1, end1, start2, end2):
                        return {"error": "选课失败，该课程上课时间与已选课程有冲突", "selected": False}
    # 考试冲突
    selct_time_sql = "select `day`,start_time,end_time from etime_slot natural join exam where `type` = 0 and etime_slot_id = (select etime_slot_id from exam where course_id = %s and sec_id = %s)"
    cursor.execute(selct_time_sql, [c_id, sec_id])
    exam_time = cursor.fetchall()
    if exam_time is None:
        return error_none
    select_selectedexam_sql = "select `day`,start_time,end_time from etime_slot natural join exam where `type` = 0 and etime_slot_id in (select etime_slot_id from exam where (course_id,sec_id) in (select course_id,sec_id from takes where s_id = %s and dropped = 0))"
    cursor.execute(select_selectedexam_sql, [s_id])
    selected_exam_time = cursor.fetchall()
    if len(selected_exam_time) != 0:
        for i in range(len(exam_time)):  # 要选课程每行判断
            day = exam_time[i][0]
            if day in [selected_exam_time[a][0] for a in range(len(selected_exam_time))]:  # 如果有新的day才判断这一行，否则跳过
                start1 = exam_time[i][1]
                end1 = exam_time[i][2]
                # print(day, start1, end1)
                for day2, start2, end2 in selected_exam_time[:]:  # 抽出该day已选课程所有的时间段
                    # print(day2, start2, end2)
                    if day2 == day and not no_conflict(start1, end1, start2, end2):
                        return {"error": "选课失败，该课程考试时间与已选课程有冲突", "selected": False}
    try:
        if insert:
            insert_sql = "insert into takes (s_id, course_id, sec_id, year, semester, dropped) values (%s, %s, %s, 2019, 1, 0)"
            cursor.execute(insert_sql, [s_id, c_id, sec_id])
        else:
            update_sql = "update takes set dropped = 0 where s_id = %s and course_id = %s and sec_id = %s "
            cursor.execute(update_sql, [s_id, c_id, sec_id])
    except Exception:
        connection.connection.rollback()
        return {"error": "选课失败，请检查您的课表或者稍后再选", "selected": False}
    return {"error": None, "selected": True}


def _applyCourse(s_id, c_id, sec_id, reason):
    error_none = {"error": "申请失败，该课程不存在", "selected": False}
    cursor = connection.cursor()
    # 已选或者退过
    check_sql = "select dropped from takes where s_id = %s and course_id = %s and sec_id = %s"
    cursor.execute(check_sql, [s_id, c_id, sec_id])
    drop = cursor.fetchone()
    insert = True
    if drop is not None:
        if drop[0] == 0:
            return {"error": "申请失败，该课程已在课表中", "selected": False}
        elif drop[0] == 1:
            return {"error": "申请失败，您已经退过该门课程，本学期不能申请", "selected": False}
    # 已经、正在申请
    check_sql = "select state from apply where s_id = %s and course_id = %s and sec_id = %s"
    cursor.execute(check_sql, [s_id, c_id, sec_id])
    state = cursor.fetchone()
    if state is not None:
        return {"error": "申请失败，您已经申请过该门课程，本学期不能申请", "selected": False}
    # 人数限制--有余量
    select_limit_sql = "select `limit` from `section` where  course_id = %s and sec_id = %s"
    cursor.execute(select_limit_sql, [c_id, sec_id])
    result = cursor.fetchone()
    if result is None:
        return error_none
    else:
        limit = result[0]
    select_num_sql = "select count(*) from takes where course_id = %s and sec_id = %s and dropped = 0"
    cursor.execute(select_num_sql, [c_id, sec_id])
    result = cursor.fetchone()
    if result is None:
        return error_none
    else:
        num = result[0]
    if num < limit:
        return {"error": "申请失败，该课程还有余量", "selected": False}
    # 人数限制--超过教室容量
    select_applied_sql = "select count(*) from apply where course_id = %s and sec_id = %s and state = 0"
    cursor.execute(select_applied_sql, [c_id, sec_id])
    result = cursor.fetchone()
    applied_num = 0
    if result is not None:
        applied_num = result[0]
    select_capacity_sql = "select capacity from `section`natural join classroom where  course_id = %s and sec_id = %s"
    cursor.execute(select_capacity_sql, [c_id, sec_id])
    result = cursor.fetchone()
    if result is None:
        return error_none
    else:
        capacity = result[0]
    if num + applied_num >= capacity:
        return {"error": "申请失败，该教室已满", "selected": False}
    # 课程冲突
    selct_time_sql = "select * from ctime_slot where  ctime_slot_id = (select ctime_slot_id from `section` where course_id = %s and sec_id = %s)"
    cursor.execute(selct_time_sql, [c_id, sec_id])
    course_time = cursor.fetchall()
    # print(course_time)
    if course_time is None:
        return error_none
    select_selectedcourse_sql = "select * from ctime_slot where  ctime_slot_id in (select ctime_slot_id from `section` where (course_id,sec_id) in (select course_id,sec_id from takes where s_id = %s and dropped = 0))"
    cursor.execute(select_selectedcourse_sql, [s_id])
    selected_course_time = cursor.fetchall()
    # print(selected_course_time)
    # print(course_time)
    if len(selected_course_time) != 0:
        for i in range(len(course_time)):  # 要选课程每行判断
            day = course_time[i][1]
            if day in [selected_course_time[a][1] for a in range(len(selected_course_time))]:  # 如果有新的day才判断这一行，否则跳过
                start1 = course_time[i][2]
                end1 = course_time[i][3]
                # print(1, day, start1, end1)
                for _, day2, start2, end2 in selected_course_time[:]:  # 抽出该day已选课程所有的时间段
                    # print(2, day2, start2, end2)
                    if day2 == day and not no_conflict(start1, end1, start2, end2):
                        return {"error": "申请失败，该课程上课时间与已选课程有冲突", "selected": False}
    # 考试冲突
    selct_time_sql = "select `day`,start_time,end_time from etime_slot natural join exam where `type` = 0 and etime_slot_id = (select etime_slot_id from exam where course_id = %s and sec_id = %s)"
    cursor.execute(selct_time_sql, [c_id, sec_id])
    exam_time = cursor.fetchall()
    if exam_time is None:
        return error_none
    select_selectedexam_sql = "select `day`,start_time,end_time from etime_slot natural join exam where `type` = 0 and etime_slot_id in (select etime_slot_id from exam where (course_id,sec_id) in (select course_id,sec_id from takes where s_id = %s and dropped = 0))"
    cursor.execute(select_selectedexam_sql, [s_id])
    selected_exam_time = cursor.fetchall()
    if len(selected_exam_time) != 0:
        for i in range(len(exam_time)):  # 要选课程每行判断
            day = exam_time[i][0]
            if day in [selected_exam_time[a][0] for a in range(len(selected_exam_time))]:  # 如果有新的day才判断这一行，否则跳过
                start1 = exam_time[i][1]
                end1 = exam_time[i][2]
                # print(day, start1, end1)
                for day2, start2, end2 in selected_exam_time[:]:  # 抽出该day已选课程所有的时间段
                    # print(day2, start2, end2)
                    if day2 == day and not no_conflict(start1, end1, start2, end2):
                        return {"error": "申请失败，该课程考试时间与已选课程有冲突", "selected": False}
    try:
        insert_sql = "insert into apply (s_id, course_id, sec_id, year, semester, `state`, apply_reason) values (%s, %s, %s, 2019, 1, 0, %s)"
        cursor.execute(insert_sql, [s_id, c_id, sec_id, reason])
    except Exception:
        connection.connection.rollback()
        return {"error": "申请失败，请检查您的课表或者稍后再选", "selected": False}
    return {"error": None, "selected": True}


def applyCourse(request):
    course_id = request.GET.get('course_id', ".")
    reason = request.GET.get('reason', "我想选课")
    c_id = course_id.split(".")[0]
    sec_id = course_id.split(".")[1]

    s_id = request.session.get('student_id', '')
    state = _applyCourse(s_id, c_id, sec_id, reason)
    return JsonResponse(state)


def selectCourse(request):
    course_id = request.GET.get('course_id', ".")
    c_id = course_id.split(".")[0]
    sec_id = course_id.split(".")[1]

    s_id = request.session.get('student_id', '')

    state = _selectCourse(s_id, c_id, sec_id)
    return JsonResponse(state)


def showSelectedCourse(request):
    s_id = request.session.get('student_id', '')

    pageSize = 10
    page = int(request.GET.get('page', 1))

    sql = "select course_id, sec_id, course_name, ctime_slot_id from `section` natural join course  where (course_id, sec_id) in (select course_id, sec_id from takes where s_id = %s and dropped = 0)"
    cursor = connection.cursor()
    cursor.execute(sql, [s_id])
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
            ctime_slot_id = results[i][3]

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
                {'course_id': course_id + '.' + str(sec_id), 'course_name': course_name, 'ctime_slot_id': ctime})

        return JsonResponse({'pageSize': pageSize, 'currentPage': page, 'totalNum': len(results), 'list': returnList})


def dejectCourse(request):
    course_id = request.GET.get('course_id', ".")
    c_id = course_id.split(".")[0]
    sec_id = course_id.split(".")[1]

    s_id = request.session.get('student_id', '')

    sql = "update takes set dropped = 1 where s_id = %s and course_id = %s and sec_id = %s"
    cursor = connection.cursor()
    try:
        cursor.execute(sql, [s_id, c_id, sec_id])
    except Exception:
        connection.connection.rollback()
        return JsonResponse({"error": "退课失败，你没有选过这门课", "dejected": False})
    return JsonResponse({"error": None, "dejected": True})


def showAppliedCourse(request):
    s_id = request.session.get('student_id', '')

    pageSize = 6
    page = int(request.GET.get('page', 1))

    sql = "select apply_reason, state, handle_reason, course_id, sec_id, course_name from apply natural join course where s_id = %s"
    cursor = connection.cursor()
    cursor.execute(sql, [s_id])
    results = cursor.fetchall()

    returnList = []

    if len(results) is 0:
        return JsonResponse({'pageSize': pageSize, 'currentPage': page, 'totalNum': 0, 'list': []})
    else:
        fromIndex = (page - 1) * pageSize
        toIndex = min(len(results), page * pageSize)

        for i in range(fromIndex, toIndex):
            apply_reason = results[i][0]
            state = int(results[i][1])
            if state == 0:
                state = "正在处理"
            elif state == 1:
                state = "申请成功"
            elif state == 2:
                state = "申请失败"
            elif state == 3:
                state = "已过期"
            handle_reason = results[i][2]
            course_id = results[i][3]
            sec_id = results[i][4]
            course_name = results[i][5]

            returnList.append(
                {'course_id': course_id + '.' + str(sec_id), 'course_name': course_name, 'reason': apply_reason,
                 'handle_reason': handle_reason, 'state': state})

        return JsonResponse({'pageSize': pageSize, 'currentPage': page, 'totalNum': len(results), 'list': returnList})


def transcript(request):
    return render(request, 'student/transcript.html')


def showTranscript(request):
    stu_id = request.session.get('student_id')

    page = int(request.GET.get('page', 1))
    pageSize = 6

    # print(course_id)
    # print(course_name)
    sql = "select course_id, sec_id, course_name, course.credits, takes.credit from course natural join main.section natural join takes where s_id = %s and takes.dropped = 0"
    cursor = connection.cursor()
    cursor.execute(sql, [stu_id])
    results = cursor.fetchall()

    returnList = []

    fromIndex = (page - 1) * pageSize
    toIndex = min(len(results), page * pageSize)
    for i in range(fromIndex, toIndex):
        result = results[i]
        grade = result[4]
        if grade is None or grade == "":
            grade = "成绩暂未公布"
        returnList.append(
            {'course_id': result[0] + '.' + str(result[1]), 'course_name': result[2], 'credit': result[3],
             'grade': grade})

    # print(returnList)
    return JsonResponse({'pageSize': pageSize, 'currentPage': page, 'totalNum': len(results), 'list': returnList})


def studentExamList(request):
    return render(request, 'student/examList.html')


def showStudentExamList(request):
    stu_id = request.session.get('student_id')

    page = int(request.GET.get('page', 1))
    pageSize = 6

    sql = "select course_id, sec_id, course_name, `type`, `day`, building, room_num, start_time, end_time from course natural join takes natural join exam natural join etime_slot where s_id = %s and takes.dropped = 0"

    cursor = connection.cursor()
    cursor.execute(sql, [stu_id])
    results = cursor.fetchall()

    returnList = []

    fromIndex = (page - 1) * pageSize
    toIndex = min(len(results), page * pageSize)
    for i in range(fromIndex, toIndex):
        result = results[i]
        c_id = result[0]
        sec_id = result[1]
        course_name = result[2]
        type = int(result[3])
        day = result[4]
        building = result[5]
        room_num = result[6]
        start_time = result[7]
        end_time = result[8]

        etime = ""
        place = ""

        if type == 0:
            type = "考试"
            etime = day + " " + str(start_time) + "-" + str(end_time)
            place = building + "." + room_num

        else:
            type = "论文"
            etime = day + " " + str(start_time)
            place = "无"

        returnList.append(
            {'course_id': c_id + '.' + str(sec_id), 'course_name': course_name, 'type': type,
             'place': place, 'etime': etime})

    # print(returnList)
    return JsonResponse({'pageSize': pageSize, 'currentPage': page, 'totalNum': len(results), 'list': returnList})
