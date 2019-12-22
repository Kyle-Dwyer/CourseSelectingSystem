import csv
import datetime

from django.db import connection, transaction
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CourseSelectingSystem.settings")


def insert_section():
    SQL_str = "SELECT distinct course_id,sec_id,building,room_num FROM (SELECT distinct * FROM jwfw)"
    cursor = connection.cursor()
    cursor.execute(SQL_str)
    domain_and_record_db_datas = cursor.fetchall()
    insert_SQL = "INSERT into `section` (course_id, sec_id, `year`, semester, building, room_num, ctime_slot_id) values (%s,%s,2019,1,%s,%s,%s)"
    print(len(domain_and_record_db_datas))
    for i in range(len(domain_and_record_db_datas)):
        print(domain_and_record_db_datas[i])
        course_id = domain_and_record_db_datas[i][0]
        sec_id = domain_and_record_db_datas[i][1]
        building = domain_and_record_db_datas[i][2]
        room_num = domain_and_record_db_datas[i][3]
        ctime_slot_id = str(i + 1)
        print((course_id, sec_id, building, room_num, ctime_slot_id,))
        cursor.execute(insert_SQL, (course_id, sec_id, building, room_num, ctime_slot_id,))


def insert_ctime_slot():
    SQL_str = "SELECT distinct course_id,sec_id,lesson,`time`,`day` FROM (SELECT distinct * FROM jwfw)"
    cursor = connection.cursor()
    cursor.execute(SQL_str)
    domain_and_record_db_datas = cursor.fetchall()
    start_time = ['8:00', '8:55', '9:55', '10:50', '11:45', '13:30', '14:25', '15:25', '16:20', '17:15', '18:30',
                  '19:25',
                  '20:20', '21:15']
    end_time = ['8:45', '9:40', '10:40', '11:35', '12:30', '14:15', '15:10', '16:10', '17:05', '18:00', '19:15',
                '20:10',
                '21:05', '22:00']
    insert_SQL = "INSERT into ctime_slot(ctime_slot_id, `day`, start_time, end_time) values (%s,%s,%s,%s)"
    print(len(domain_and_record_db_datas))
    for i in range(len(domain_and_record_db_datas)):
        print(domain_and_record_db_datas[i])
        lesson = int(domain_and_record_db_datas[i][2])
        day = domain_and_record_db_datas[i][4]
        start = int(domain_and_record_db_datas[i][3].split('-')[0])
        end = int(domain_and_record_db_datas[i][3].split('-')[1])
        for j in range(start - 1, end):
            print((str(i + 1), day, start_time[j], end_time[j]))
            cursor.execute(insert_SQL, (str(i + 1), day, start_time[j], end_time[j],))
        connection.connection.commit()


def insert_teaches():
    SQL_str = "SELECT distinct course_id,sec_id,instructor_name FROM (SELECT distinct * FROM jwfw)"
    cursor = connection.cursor()
    cursor.execute(SQL_str)
    domain_and_record_db_datas = cursor.fetchall()
    insert_SQL = "INSERT into teaches (i_id,course_id, sec_id, `year`, semester) values ((SELECT i_id from instructor where  name = %s),%s,%s,2019,1)"
    print(len(domain_and_record_db_datas))
    for i in range(len(domain_and_record_db_datas)):
        print(domain_and_record_db_datas[i])
        course_id = domain_and_record_db_datas[i][0]
        sec_id = domain_and_record_db_datas[i][1]
        instructor_name = domain_and_record_db_datas[i][2]

        print((course_id, sec_id, instructor_name,))
        cursor.execute(insert_SQL, (instructor_name, course_id, sec_id,))


def insert_etime_slot():
    sql1 = "insert into etime_slot (etime_slot_id, start_time, end_time) values (%s, %s, %s)"
    cursor = connection.cursor()

    sql2 = "select * from main.section"
    cursor.execute(sql2)
    result2 = cursor.fetchall()
    if len(result2) != 0:
        for i in result2:
            with transaction.atomic():
                course_id, sec_id, year, semester, building, room_num, ctime_slot_id, limit = i
                etime_slot_id = ctime_slot_id
                sql3 = "select * from ctime_slot where ctime_slot_id = %s"
                cursor.execute(sql3, [ctime_slot_id])
                result3 = cursor.fetchone()
                ctime_slot_id, c_day, c_start_time, c_end_time = result3
                e_start_time = c_start_time.strftime('%H:%M:%S')
                hour = (c_start_time.hour + 2)
                e_end_time = c_start_time.replace(hour=hour).strftime('%H:%M:%S')
                # print([etime_slot_id, e_start_time, e_end_time])
                cursor.execute(sql1, [etime_slot_id, e_start_time, e_end_time])

                sql4 = "insert into exam (course_id, sec_id, `year`, semester, `type`, `day`, etime_slot_id, building, room_num) values (%s, %s, 2019, 1, 0, %s, %s, %s, %s)"
                cursor.execute(sql4, [course_id, sec_id, c_day, etime_slot_id, building, room_num])


def make_section_excel():
    sql = "select course_id, sec_id, `year`, semester, building, room_num, `limit`, exam.day, etime_slot.start_time, etime_slot.end_time, i_id, `type`, ctime_slot_id from teaches natural join `section` natural join etime_slot natural join exam"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    print(len(result))
    write_file = open("../data/section_final.csv", 'w',
                      newline='', encoding='UTF-8')

    writer = csv.writer(write_file)

    writer.writerow(["course_id", "sec_id", "year", "semester", "building", "room_num", "limit", "etime_slot.day",
                     "etime_slot.start_time", "etime_slot.end_time", "i_id",  "type", "course_name","credits","dept_name", "ctime_slot.day",
                     "ctime_slot.start_time", "ctime_slot.end_time"])

    print()
    for r in result:
        course_id = r[0]
        c_s_i = r[-1]
        sql2 = "select course_name,credits,dept_name from course where course_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql2, [course_id])
        result = cursor.fetchone()
        course_name = result[0]
        credit = result[1]
        dept_name = result[2]
        sql3 = "select `day`, start_time, end_time from ctime_slot where ctime_slot_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql3, [c_s_i])
        c_s = cursor.fetchall()
        s, e, d = "", "", ""
        for i in c_s:
            s += str(i[1]) + "|"
            e += str(i[2]) + "|"
            d += str(i[0]) + "|"
        writer.writerow(r[:-1] + (course_name, credit, dept_name, d, s, e))


def make_student_excel():
    sql = "select s_id, password, name, dept_name, phone_num, tot_cred from account, student where user_id = s_id"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    write_file = open("../data/student.csv", 'w',
                      newline='', encoding='UTF-8')

    writer = csv.writer(write_file)

    writer.writerow(["s_id", "password", "name", "dept_name", "phone_num", "tot_cred"])

    for r in result:
        writer.writerow(r)


def make_teacher_excel():
    sql = "select i_id, password, name, dept_name, phone_num, salary from account, instructor where user_id = i_id"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    write_file = open("../data/instructor.csv", 'w',
                      newline='', encoding='UTF-8')

    writer = csv.writer(write_file)

    writer.writerow(["i_id", "password", "name", "dept_name", "phone_num", "salary"])

    for r in result:
        writer.writerow(r)

def dicfetchall(cursor):
    "return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


from collections import namedtuple


def namedturplefetchall(cursor):
    "return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    nt_result = namedtuple('Result', columns)
    return [
        nt_result(*row)
        for row in cursor.fetchall()
    ]


if __name__ == '__main__':
    make_teacher_excel()
