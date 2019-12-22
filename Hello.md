# 项目文档（《数据库设计》课程）

## 选课系统数据库设计



## 功能点实现
###学生模块
##### 信息查看和修改
学生登录后，跳转至个人信息页面，可以修改个人信息（目前只有联系电话可以修改）
#### 课程表
在正常学期内，学生可以查看课程表，我们既实现了课程表UI，又附带课程表表格
#### 选/退课
在选课期间内，学生可以选退课，我们将所有可选课程以列表形式呈现出来，学生可以通过课程代码和名称搜索到相应课程，学生选课限制检查：  
+ 该课程已在该学期课程表中
+ 该课程人数已满
+ 该课程上课时间与已选课程有冲突
+ 该课程考试时间与已选课程有冲突  

学生可以在同一页面看到自己已选课程，可以点击退课
#### 选课申请
在选课期间内，学生可以选课申请，我们将所有可选课程以列表形式呈现出来，学生可以通过课程代码和名称搜索到相应课程，学生选课申请限制检查：  
+ 该课程已在该学期课程表中
+ 该课程已在该学期被退过
+ 该课程已在该学期被申请过
+ 该课程有余量
+ 该课程教室已满（已选人数+已申请人数）
+ 该课程上课时间与已选课程有冲突
+ 该课程考试时间与已选课程有冲突  
#### 学生查看自己的考试
学生登录后，可以查看自己的考试信息
#### 查看分数
学生登录后，可以查看自己的成绩单

### 教师模块
#### 信息修改
教师登录后，跳转至个人信息页面，可以修改个人信息（目前只有联系电话可以修改）
#### 查看已开和课程花名册
教师登录后，可以查看看自己已开设的课程，可以点进花名册，并在考试期间单个登分
#### 处理选课申请
在选课期间，教师可以处理选课申请，同意或拒绝，选课结束后再处理会因为过期而处理失败
#### 课程添加
教师登录后，可以手动添加课程，教师开课限制检查：  
+ 该课程（course）如果已存在，信息是否正确
+ 该课程时间段合法
+ 该课程与教师已开课程上课时间冲突
+ 该课程的上课时间地点与本学期其他课程是否冲突
+ 该课程的考试时间地点与本学期其他课程是否冲突
+ 该课程人数上限是否超过教室上限 
#### 人工登分
教师登录后，可以点进花名册，并在考试期间单个登分
#### 自动登分
在考试期间，教师可以excel自动登分，登分限制检查：  
+ 分数不合法
+ 登分课程不是该教师开的课
+ 该学生不未选该课程

### 管理员
#### 学生查看、添加
管理员登录后，可以excel导入学生信息
#### 教师查看、添加
管理员登录后，可以excel导入教师信息
#### 课程添加
管理员登录后，可以excel自动添加课程，开课限制检查：  
+ 该课程（course）如果已存在，信息是否正确
+ 该课程时间段合法
+ 该课程与教师已开课程上课时间冲突
+ 该课程的上课时间地点与本学期其他课程是否冲突
+ 该课程的考试时间地点与本学期其他课程是否冲突
+ 该课程人数上限是否超过教室上限 
#### 课程删除
在选课期间，管理员可以删除某门课程
#### 登分
在考试期间，管理员可以excel自动登分，登分限制检查：  
+ 分数不合法
+ 登分课程不是该教师开的课
+ 该学生不未选该课程
#### 时间段
管理员登录后，可以改变时间段，分别为选课期和考试期

## 表结构
+ course: 
```sqlite
create table course
(
   course_id varchar(10) not null
      primary key,
   course_name varchar(128) not null,
   credits integer default 0 not null,
   dept_name varchar(128) not null
);
```

+ section: 
```sqlite
create table section
(
   course_id varchar(128) not null
      references course
         on update cascade on delete cascade,
   sec_id integer not null,
   year varchar(4) not null,
   semester integer(1) not null,
   building varchar(128) default 0 not null,
   room_num varchar(10) default 0 not null,
   ctime_slot_id INTEGER,
   "limit" integer default 0 not null,
   primary key (course_id, sec_id, year, semester),
   foreign key (building, room_num) references classroom
      on update cascade on delete cascade,
   constraint check_semester
      check (semester in (1,2))
);
```
+ account: 
```sqlite
create table account
(
   account_id INTEGER not null
      primary key autoincrement,
   user_id varchar(10) not null
      unique,
   password varchar(128) not null,
   role integer(1) not null,
   check (role in (0,1,2))
);
```
+ student: 
```sqlite
create table student
(
   s_id varchar(10) not null
      primary key
      references account (user_id)
         on update cascade on delete cascade,
   name varchar(128) not null,
   dept_name varchar(128) not null,
   phone_num varchar(15),
   tot_cred integer default 0 not null
);
```
+ instructor: 
```sqlite
create table instructor
(
   i_id varchar(10) not null
      primary key
      references account (user_id)
         on update cascade on delete cascade,
   name varchar(128) not null,
   dept_name varchar(128) not null,
   phone_num varchar(15),
   salary integer default 0 not null
);
```
+ exam: 
```sqlite
create table exam
(
   course_id varchar(128) not null,
   sec_id integer not null,
   year varchar(128) not null,
   semester integer(1) not null,
   type integer(1) default 0 not null,
   day enum not null,
   etime_slot_id INTEGER not null
      references etime_slot
         on update cascade on delete cascade,
   building varchar(128),
   room_num varchar(10) default 0,
   primary key (course_id, sec_id, year, semester),
   foreign key (course_id, sec_id, year, semester) references section
      on update cascade on delete cascade,
   foreign key (building, room_num) references classroom
      on update cascade on delete cascade,
   constraint check_day
      check (day in ('Mon', 'Tue', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun')),
   constraint check_type
      check (type in (0, 1))
);
```
+ classroom: 
```sqlite
create table classroom
(
   building varchar(128) not null,
   room_num varchar(10) default 0 not null,
   capacity integer default 0 not null,
   primary key (building, room_num)
);
```
+ teaches: 
```sqlite
create table teaches
(
   i_id INTEGER not null
      references instructor
         on update cascade on delete cascade,
   course_id varchar(128) not null,
   sec_id integer not null,
   year varchar(4) not null,
   semester integer(1) not null,
   primary key (i_id, course_id, sec_id, year, semester),
   foreign key (course_id, sec_id, year, semester) references section
      on update cascade on delete cascade
);
```
+ takes: 
```sqlite
create table takes
(
   s_id INTEGER not null
      references student
         on update cascade on delete cascade,
   course_id varchar(128) not null,
   sec_id integer not null,
   year varchar(4) not null,
   semester integer(1) not null,
   dropped integer(1) default 0 not null,
   credit integer,
   primary key (s_id, course_id, sec_id, year, semester),
   foreign key (course_id, sec_id, year, semester) references section
      on update cascade on delete cascade,
   constraint check_drop
      check (dropped in (0,1))
);
```
+ apply: 
```sqlite
create table apply
(
   apply_id INTEGER not null
      primary key autoincrement,
   s_id varchar(10) not null
      references student
         on update cascade on delete cascade,
   apply_reason varchar(128),
   state integer(1) default 0 not null,
   handle_reason varchar(128),
   course_id varchar(128) not null,
   sec_id integer not null,
   year varchar(4) not null,
   semester integer(1),
   foreign key (course_id, sec_id, year, semester) references section
      on update cascade on delete cascade,
   constraint check_state
      check (state in (0,1,2,3))
);
```
+ ctime_slot: 
```sqlite
create table ctime_slot
(
   ctime_slot_id INTEGER not null,
   day enum not null,
   start_time time(10) not null,
   end_time time(10) not null,
   primary key (ctime_slot_id, day, start_time),
   constraint check_day
      check (day in ('Mon','Tue','Wed','Thurs','Fri','Sat','Sun'))
);
```
+ e_time_slot: 
```sqlite
create table etime_slot
(
   etime_slot_id INTEGER not null
      primary key autoincrement,
   start_time time(10) not null,
   end_time time(10) not null
);
```