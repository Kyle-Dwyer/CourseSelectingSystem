from django.db import connection
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
    start_time = ['8:00', '8:55', '9:55', '10:50', '11：45', '13:30', '14:25', '15:25', '16:20', '17:15', '18:30',
                  '19:25',
                  '20:20', '21:15']
    end_time = ['8:45', '9:40', '10:40', '11:35', '12：30', '14:15', '15:10', '16:10', '17:05', '18:00', '19:15',
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
