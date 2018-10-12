#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: _wapn

import cx_Oracle
import requests
import redis
from flask import Flask, request

app = Flask(__name__)


@app.route('/')  # 默认get请求
def show():
    return '''   
    <script>
        function inputDialog(type){

            if(type==1){
                var inputContent  = prompt("请输入订单编号：")
                if(!inputContent){
                    return;
                }
                location.href = 'http://192.168.5.91:5000/delete/orderdata2?order_no='+inputContent;
            }

            if(type==2){
                var inputContent  = prompt("请输入用户编号：")
                if(!inputContent){
                    return;
                }
                location.href='http://192.168.5.91:5000/delete/orderdata?user_id=' + inputContent;
            }

            if(type==3){
                var inputContent  = prompt("请输入用户编号：")
                if(!inputContent){
                    return;
                }
                location.href='http://192.168.5.91:5000/delete/user?user_id=' + inputContent;
            }
            
            if(type==4){
            var inputContent = prompt("请输入活动编号：")
            if(!inputContent){
            return;
            }
            location.href='http://192.168.5.91:5000/update/week?activity_id=' + inputContent;
            }
            
             if(type==5){
            var inputContent = prompt("请输入活动编号：")
            if(!inputContent){
            return;
            }
            location.href='http://192.168.5.91:5000/delete/week?activity_id=' + inputContent;
            }
            
             if(type==6){
            var inputContent = prompt("请输入活动编号：")
            if(!inputContent){
            return;
            }
            location.href='http://192.168.5.91:5000/update/date?activity_id=' + inputContent;
            }
        }
    </script> 
    
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>测试专用</title>
    
</head>

<body>
 <u1>
    <h1>测试数据</h1>
    <li><a onclick="inputDialog(1)">按订单号删除数据</a></li> 
    <li><a onclick="inputDialog(2)">按用户编号删数据</a></li> 
    <li><a onclick="inputDialog(3)">删用户清缓存</a></li> 
    <li><a onclick="inputDialog(4)">输入活动编号清除redis数据并更新周四活动，2分钟后开始</a></li> 

    <li><a onclick="inputDialog(6)">输入活动编号更新天天送礼活动，10秒后开始</a></li>
    </u1>
    <u1>
    <h1>资料查询</h1> 
    <li><a href='http://www.w3school.com.cn'>W3school</a></li>  
    <li><a href='https://www.baidu.com'>百度一下</a></li>
    <li><a href='https://yuedu.baidu.com/customer/mybook'>百度阅读</a></li>
    <li><a href='https://www.cnblogs.com/wapn'>wapn的博客</a></li>
    </u1>
</body>
</html> 
   '''


# 清除数据及删用户，清缓存
@app.route('/delete/userdata', endpoint='delete', methods=['GET', 'POST', 'PUT'])
def show_user_profile():
    print(request.method)
    if request.method == 'GET':
        # id1 = request.args.get('user_id')  # get请求参数读取
        # id2 = eval(id1)               # str转换int
        id2 = request.args['user_id']
        result1 = delete(id2)
        result2 = req(id2)
        return result1 + result2
    elif request.method == 'POST':
        id2 = request.form['user_id']
        result1 = delete(id2)
        result2 = req(id2)
        return result1 + result2
    else:
        return ''


# 仅删用户，清缓存
@app.route('/delete/user', endpoint='deleteuser', methods=['GET', 'POST', 'PUT'])
def show_user_profile():
    print(request.method)
    if request.method == 'GET':
        id2 = request.args['user_id']
        result1 = deleteuser(id2)
        result2 = req(id2)
        return result1 + result2
    elif request.method == 'POST':
        id2 = request.form['user_id']
        result1 = deleteuser(id2)
        result2 = req(id2)
        return result1 + result2
    else:
        return ''


# 按订单编号清除订单数据
@app.route('/delete/orderdata2', endpoint='orderdata2', methods=['GET', 'POST', 'PUT'])
def show_user_profile():
    print(request.method)
    if request.method == 'GET':
        id2 = request.args['order_no']
        result1 = deletedata(id2)
        return result1
    elif request.method == 'POST':
        id2 = request.form['order_no']
        result1 = deletedata(id2)
        return result1
    else:
        return ''


# 按活动编号更新周四数据，5分钟后活动开始
@app.route('/update/week', endpoint='week', methods=['GET', 'POST', 'PUT'])
def show_user_profile():
    print(request.method)
    if request.method == 'GET':
        id2 = request.args['activity_id']
        result1 = updateweek(id2)
        return result1
    elif request.method == 'POST':
        id2 = request.form['activity_id']
        result1 = updateweek(id2)
        return result1
    else:
        return ''


# 按活动编号删除周四数据
@app.route('/delete/week', endpoint='week1', methods=['GET', 'POST', 'PUT'])
def show_user_profile():
    print(request.method)
    if request.method == 'GET':
        id2 = request.args['activity_id']
        result1 = deleteweek(id2)
        return result1
    elif request.method == 'POST':
        id2 = request.form['activity_id']
        result1 = deleteweek(id2)
        return result1
    else:
        return ''


# 按活动编号更新天天送礼活动
@app.route('/update/date', endpoint='date', methods=['GET', 'POST', 'PUT'])
def show_user_profile():
    print(request.method)
    if request.method == 'GET':
        id2 = request.args['activity_id']
        result1 = updatedate(id2)
        return result1
    elif request.method == 'POST':
        id2 = request.form['activity_id']
        result1 = updatedate(id2)
        return result1
    else:
        return ''


# 按用户编号清订单数据
@app.route('/delete/orderdata', endpoint='orderdata', methods=['GET', 'POST', 'PUT'])
def show_user_profile():
    # print(url_for('v_contacts', _anchor='part'))
    print(request.method)
    if request.method == 'GET':
        id2 = request.args['user_id']
        result3 = deletedata_(id2)
        return result3
    elif request.method == 'POST':
        id2 = request.form['user_id']
        result3 = deletedata_(id2)
        return result3
    else:
        return ''


# 清缓存
def req(id2):
    r = requests.get('https://xiaowei.100bm.cn/user/delete/session?user_ids=' + str(id2))
    print(r.status_code)
    return '+清除缓存'


# 按用户编号删用户及订单数据
def delete(id2):
    # 链接数据库
    conn = cx_Oracle.connect('czth_sales/123456@192.168.0.136:1521/ORCL136')
    cur = conn.cursor()
    try:
        # 执行sql语句
        sql = '''
            declare
              c_user_id number(20) := %s;
            begin
              delete th_wx_payment where user_id = c_user_id;
              delete th_order_main_ext
               where order_no in
                     (select order_no from th_order_info where user_id = c_user_id);
              delete th_order_delivery_query
               where order_no in
                     (select order_no from th_order_info where user_id = c_user_id);
              delete th_order_delivery_ext
               where order_no in
                     (select order_no from th_order_info where user_id = c_user_id);
              delete th_order_info where user_id = c_user_id;
              delete th_user_info where user_id = c_user_id;
              commit;
            end;
            ''' % id2
        cur.execute(sql)
        conn.commit()
        return '删除成功' + sql
    except:
        return 'sql执行异常'


# 按订单编号删订单数据
def deletedata(id2):
    # 链接数据库
    conn = cx_Oracle.connect('czth_sales/123456@192.168.0.136:1521/ORCL136')
    cur = conn.cursor()
    try:
        # 执行sql语句
        sql = ''' declare
                c_order_no varchar2(32):='%s';
                begin
                delete th_order_info where order_no =c_order_no;
                delete th_wx_payment where order_no =c_order_no;
                delete th_order_main_ext where order_no =c_order_no;
                delete th_order_delivery_ext where order_no =c_order_no;
                delete th_order_delivery_query where order_no =c_order_no;
                delete th_order_goods_ext where order_no =c_order_no;
                delete th_order_product_detail where order_no =c_order_no;
                commit;
                end;
                ''' % id2
        cur.execute(sql)
        conn.commit()

        return '删除成功' + sql
    except:
        return 'sql执行异常'


# 删用户
def deleteuser(id2):
    # 链接数据库
    conn = cx_Oracle.connect('czth_sales/123456@192.168.0.136:1521/ORCL136')
    cur = conn.cursor()
    try:
        # 执行sql语句
        sql = '''delete th_user_info where user_id =%s''' % str(id2)
        cur.execute(sql)
        conn.commit()
        return '删除成功' + sql
    except:
        return 'sql执行异常'


# 按用户编号删数据
def deletedata_(id2):
    # 链接数据库
    conn = cx_Oracle.connect('czth_sales/123456@192.168.0.136:1521/ORCL136')
    cur = conn.cursor()

    try:
        sql = ''' 
            declare
              c_user_id number(20) := %s;
            begin
            update th_goods_card_info
                 set status           = 0,
                     occupy_flow_time = null,
                     occupy_user_id   = null,
                     occupy_order_no  = null
               where occupy_user_id = c_user_id;
              update th_user_info set kingcard_user = 1 where user_id = c_user_id;
              delete th_order_main_ext
               where order_no in
                     (select order_no from th_order_info where user_id = c_user_id);
              delete th_order_delivery_query
               where order_no in
                     (select order_no from th_order_info where user_id = c_user_id);
              delete th_order_delivery_ext
               where order_no in
                     (select order_no from th_order_info where user_id = c_user_id);
              delete th_order_info where user_id = c_user_id;
              delete th_order_goods_ext where user_id = c_user_id;
              delete th_user_goods_info where user_id = c_user_id;
              delete th_vouchers_recv where user_id = c_user_id;
              delete th_wx_payment where user_id = c_user_id;
              delete fd_fund_account where user_id = c_user_id;
              delete fd_fund_change where user_id = c_user_id;
              delete fd_cash_apply where user_id = c_user_id;
              delete th_order_info
               where order_no in (select e.order_no
                                    from th_order_main_ext e
                                   where e.promote_user_id = c_user_id);
              delete th_order_main_ext where promote_user_id = c_user_id;
              commit;
            end;

        ''' % str(id2)

        cur.execute(sql)
        conn.commit()
        return '删除成功' + sql
    except:
        return 'sql执行异常'


# 清除redis，按活动编号更新周四活动，2分钟后开始
def updateweek(id2):
    # 清除redis周四特惠数据
    r = redis.StrictRedis(host='192.168.0.116', port=6379, db=0)
    t = r.keys('th:{th_week}*')
    for i in t:
        r.delete(i)
    # 链接数据库
    conn = cx_Oracle.connect('czth_sales/123456@192.168.0.136:1521/ORCL136')
    cur = conn.cursor()
    try:
        sql = '''
            declare
              c_activity_id number(20) := %s;
            begin
              update th_week_activity_info
                 set status      = 1,
                     start_time  = sysdate + 2 / 24 / 60,
                     end_time    = sysdate + 1 / 24,
                     activity_id = c_activity_id
               where activity_id = c_activity_id;
              update th_week_activity_product
                 set status = 1, activity_id = c_activity_id
               where activity_id = c_activity_id;
              commit;
            end;
        ''' % str(id2)
        cur.execute(sql)
        conn.commit()
        return '更新成功' + sql
    except:
        return 'sql执行异常'


# 按活动编号删除周四活动
def deleteweek(id2):
    # 清除redis周四特惠数据
    r = redis.StrictRedis(host='192.168.0.116', port=6379, db=0)
    t = r.keys('th:{th_week}*')
    for i in t:
        r.delete(i)
    # 链接数据库
    conn = cx_Oracle.connect('czth_sales/123456@192.168.0.136:1521/ORCL136')
    cur = conn.cursor()
    try:
        sql = '''
            declare
            c_activity_id number(20):=%s;
            begin
            delete th_week_activity_info where activity_id=c_activity_id;
            delete th_week_activity_product where activity_id=c_activity_id;
            delete th_week_activity_recv where activity_id=c_activity_id;
            delete th_week_activity_remind where activity_id=c_activity_id;
            commit;
            end;
            ''' % str(id2)
        cur.execute(sql)
        conn.commit()
        return '删除成功' + sql
    except:
        return 'sql执行异常'


# 按活动编号更新天天送礼活动
def updatedate(id2):
    # 链接数据库
    conn = cx_Oracle.connect('czth_sales/123456@192.168.0.136:1521/ORCL136')
    cur = conn.cursor()
    try:
        sql = '''
            declare
              c_activity_id number(20) := %s;
            begin
              update th_partner_activity_info t
                 set t.status            = 20,
                     t.prize_open_status = 1,
                     t.join_count        = 0,
                     start_time          = sysdate + 10 / 24 / 60 / 60,
                     end_time            = sysdate + 5 / 24
               where t.activity_id = c_activity_id;
              update th_partner_prize_info t
                 set t.status = 1
               where t.activity_id = c_activity_id;
              delete th_partner_activity_details t where t.activity_id = c_activity_id;
              delete th_vouchers_recv t where t.activity_id = c_activity_id;
              commit;
            end;
            ''' % str(id2)
        cur.execute(sql)
        conn.commit()
        return '更新成功' + sql
    except:
        return 'sql执行异常'


# if __name__ == '__main__':
app.run(host='192.168.5.91')
