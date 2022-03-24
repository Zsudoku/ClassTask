'''
Date: 2022-03-24 11:08:30
LastEditors: ZSudoku
LastEditTime: 2022-03-24 16:58:24
FilePath: \ClassTask\task_v1.0-git.py
'''
import datetime
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import schedule
classTaskLis = [
                [['测试课程1',2,9,'基础楼108','16:05','16:06'],['测试课程2',2,9,'基础楼108','16:22','16:25']],#周一
                [['测试课程1',2,9,'基础楼108','16:05','16:06'],['测试课程2',2,9,'基础楼108','16:22','16:25']],#周二
                [['测试课程1',2,9,'基础楼108','16:05','16:06'],['测试课程2',2,9,'基础楼108','16:22','16:25']],#周三
                [['测试课程1',2,9,'基础楼108','16:05','16:06'],['测试课程2',2,9,'基础楼108','16:22','16:25']],#周四
                [['测试课程1',2,9,'基础楼108','16:05','16:06'],['测试课程2',2,9,'基础楼108','16:22','16:25']],#周五
                ] 
#当前校历周
weeks = 6
#发邮件
def send_mail(tx,tittle,rev,rev_name,sen_name):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user="xxxx@qq.com"    #用户名
    mail_pass="xxxx"   #口令 
    sender = 'xxxx@qq.com'
    receivers = [rev]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    message = MIMEText(tx)
    message['From'] = Header(sen_name, 'utf-8') #括号里的对应发件人邮箱昵称（随便起）、发件人邮箱账号
    message['To'] = Header(rev_name, 'utf-8') #括号里的对应收件人邮箱昵称、收件人邮箱账号
    subject = tittle
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 587)  # 发件人邮箱中的SMTP服务器，端口是465
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
        return "success"
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
        return "error"

#计算两个日期之间的天数
def computeDays(day1, day2):
    time_array1 = time.strptime(day1, "%Y-%m-%d")
    timestamp_day1 = int(time.mktime(time_array1))
    time_array2 = time.strptime(day2, "%Y-%m-%d")
    timestamp_day2 = int(time.mktime(time_array2))
    result = (timestamp_day2 - timestamp_day1) // 60 // 60 // 24
    return result
#根据天数计算当前周数
def computeWeek(result,weeks):
    if(result>6):
        weeks += int(result/7)
    return weeks
# print(dayOfWeek)
def job(days,i):
    tx = '课程名称为：'+ classTaskLis[days-1][i][0] + '上课地点为：' + classTaskLis[days-1][i][3] + '上课时间为：' + classTaskLis[days-1][i][5]
    send_mail(tx,'课程通知','xxxx@qq.com','xxx','自动化课程表')
    print("working...")
    return schedule.CancelJob
    
def daysJob(days):
    for i in range(len(classTaskLis[days-1])):
        
        #判断是否在该周上课
        if (weeks+1>classTaskLis[days-1][i][1] and weeks-1<classTaskLis[days-1][i][2] ):
            string = classTaskLis[days-1][i][4]
            classTime = datetime.datetime.strptime(string,'%H:%S')
            #classTime = classTime.hour
            nowTime = datetime.datetime.now()
            #nowTime = nowTime.hour
            if(nowTime.hour > classTime.hour):
                continue
            if(nowTime.hour == classTime.hour):
                if(nowTime.minute > classTime.minute):
                    continue
            print(classTaskLis[days-1][i][4])
            schedule.every().day.at(classTaskLis[days-1][i][4]).do(job,days=days,i=i)
            while True:
                #print("wait...")
                schedule.run_pending()
                time.sleep(0.5)
                time1 = datetime.datetime.now()
                time1 = datetime.datetime.strftime(time1,'%H:%M')
                if((time1 == classTaskLis[days-1][i][5])):
                    print("break")
                    break
        else:
            print(classTaskLis[days-1][i][0],"周数不对")
def start():
    #判断今天是周几
    dayOfWeek = datetime.datetime.now().isoweekday() ###返回数字1-7代表周一到周日
    if(dayOfWeek>5):
        print("休息日")
        tx = "今天没课，早些休息！"
        send_mail(tx,'今日课程','xxxx@qq.com','xxx','自动化课程表')
        time.sleep(1000)
    else:
        print("有课")
        tx = str(classTaskLis[dayOfWeek-1])
        send_mail(tx,'今日课程','xxxx@qq.com','xxx','自动化课程表')
        time.sleep(1)
        daysJob(dayOfWeek)
    return schedule.CancelJob

if __name__ == '__main__':
    weeks = computeWeek(computeDays(day1="2022-03-21",day2=datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d')),weeks)
    print("weeks:",weeks)
    while True:
        schedule.every().day.at("00:00").do(start)
        time.sleep(1)