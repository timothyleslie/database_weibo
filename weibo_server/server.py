# -*- coding: utf-8 -*-
import pymysql
from flask import Flask, request, jsonify
from flask_cors import CORS

# 数据库连接
db = pymysql.connect("127.0.0.1", "root", "MySQL123456", "weibo")
cursor = db.cursor()

# 后端服务启动
app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route('/login/add', methods=['POST'])
def login_add():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            cursor.execute("insert into user(U_NAME,U_PASSWORD) values (\""
                           + str(username) + "\",\"" + str(password) + "\")")
            db.commit()  # 提交，使操作生效
            print("add a new user successfully!")
            cursor.execute("select U_ID, U_NAME from user where U_NAME=\""
                       + str(username) + "\" and U_PASSWORD=\"" + str(password) + "\"")
            data = cursor.fetchone()
            if (data != None):
                print("result:", data)
                jsondata = {"id": str(data[0]), "username": str(data[1]),
                            }
                return jsonify(jsondata)
            else:
                print("result: NULL")
                jsondata = {}
            return jsonify(jsondata)
        except Exception as e:
            print("add a new user failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


@app.route('/login/login', methods=['POST'])
def login_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print(username, password)
        cursor.execute("select U_ID, U_NAME from user where U_NAME=\""
                       + str(username) + "\" and U_PASSWORD=\"" + str(password) + "\"")
        data = cursor.fetchone()
        if (data != None):
            print("result:", data)
            jsondata = {"id": str(data[0]), "username": str(data[1]),
                        }
            return jsonify(jsondata)
        else:
            print("result: NULL")
            jsondata = {}
            return jsonify(jsondata)


@app.route('/login/update', methods=['POST'])
def login_update():
    if request.method == "POST":
        id = request.form.get("id")
        password = request.form.get("password")
        try:
            cursor.execute("update user set U_PASSWORD=\"" + str(password)
                           + "\" where U_ID=" + str(id))
            db.commit()
            print("update password successfully!")
            return "1"
        except Exception as e:
            print("update password failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


@app.route('/login/del', methods=['POST'])
def login_del():
    if request.method == "POST":
        id = request.form.get("id")
        try:
            cursor.execute("delete from user where U_ID=" + str(id))
            db.commit()
            print("delete user" + str(id) + " successfully!")
            return "1"
        except Exception as e:
            print("delete the user failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


@app.route('/article/list', methods=['POST'])
def article_list():
    if request.method == "POST":
        uid = request.form.get("uid")
        print('uid:' + str(uid))
        if uid == "0":  # 查询全部公开的收藏数据
            # cursor.execute("select A_ID,U_NAME,A_CONTENT,A_TIME, LIKE_CNT, FAVORITE_CNT, COMMENT_CNT from user, article "
            #                + "where user.U_ID = article.U_ID order by A_TIME desc")
            cursor.execute("select * from view_article")
        else:
            cursor.execute("select  A_ID,U_NAME,A_CONTENT,A_TIME, LIKE_CNT, FAVORITE_CNT, COMMENT_CNT from user, article "
                           + "where article.U_ID=" + str(uid) + " and user.U_ID=article.U_ID order by A_TIME desc")
        data = cursor.fetchall()
        temp = {}
        result = []
        if (data != None):
            for i in data:
                temp["id"] = i[0]
                temp["wname"] = i[1]
                temp["content"] = i[2]
                temp["ctime"] = i[3]
                temp["like_cnt"] = i[4]
                temp['favorite_cnt'] = i[5]
                temp['comment_cnt'] = i[6]
                result.append(temp.copy())  # 特别注意要用copy，否则只是内存的引用
            print("result:", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])


@app.route('/article/follow', methods=['POST'])
def article_follow():
    if request.method == "POST":
        uid = request.form.get("uid")
        print('uid:' + str(uid))

        cursor.execute("select  A_ID,U_NAME,A_CONTENT,A_TIME, LIKE_CNT, FAVORITE_CNT, COMMENT_CNT from user, article "
                       + "where article.U_ID in "
                         "(select CONCERNED_U_ID from concern where CONCERN_U_ID= " + str(uid) + ")"
                       + " and user.U_ID=article.U_ID order by A_TIME desc")
        data = cursor.fetchall()
        temp = {}
        result = []
        if (data != None):
            for i in data:
                temp["id"] = i[0]
                temp["wname"] = i[1]
                temp["content"] = i[2]
                temp["ctime"] = i[3]
                temp["like_cnt"] = i[4]
                temp['favorite_cnt'] = i[5]
                temp['comment_cnt'] = i[6]
                result.append(temp.copy())  # 特别注意要用copy，否则只是内存的引用
            print("result:", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])


@app.route('/article/search', methods=['POST'])
def article_search():
    if request.method == "POST":
        content = request.form.get("content")
        print('content:' + str(content))

        cursor.execute("select  A_ID,U_NAME,A_CONTENT,A_TIME, LIKE_CNT, FAVORITE_CNT, COMMENT_CNT from user, article "
                       + "where article.U_ID=user.U_ID and article.A_CONTENT like '%" + str(content) + "%\'")
        data = cursor.fetchall()
        temp = {}
        result = []
        if (data != None):
            for i in data:
                temp["id"] = i[0]
                temp["wname"] = i[1]
                temp["content"] = i[2]
                temp["ctime"] = i[3]
                temp["like_cnt"] = i[4]
                temp['favorite_cnt'] = i[5]
                temp['comment_cnt'] = i[6]
                result.append(temp.copy())  # 特别注意要用copy，否则只是内存的引用
            print("result:", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])


@app.route('/article/add', methods=['POST'])
def article_add():
    if request.method == "POST":
        uid = request.form.get("uid")
        content = request.form.get("content")
        try:
            cursor.execute("insert into article(U_ID, A_CONTENT) values (\""
                           + str(uid) + "\",\""
                           + str(content) + "\")")
            db.commit()  # 提交，使操作生效
            print("add a new article successfully!")
            return "1"
        except Exception as e:
            print("add a new article failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


@app.route('/article/del', methods=['POST'])
def article_del():
    if request.method == "POST":
        id = request.form.get("id")
        try:
            cursor.execute("delete from article where A_ID=" + str(id))
            db.commit()
            print("delete article" + str(id) + " successfully!")
            return "1"
        except Exception as e:
            print("delete the article failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


@app.route('/favorite/update', methods=['POST'])
def article_update():
    if request.method == "POST":
        id = request.form.get("id")
        wname = request.form.get("wname")
        wurl = request.form.get("wurl")
        _type = request.form.get("type")
        try:
            cursor.execute("update favorite set wname=\"" + str(wname)
                           + "\", wurl=\"" + str(wurl) + "\", type=\""
                           + str(_type) + "\" where id=" + str(id))
            db.commit()
            print("update favorite successfully!")
            return "1"
        except Exception as e:
            print("update favorite failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


@app.route('/favorite/count', methods=['POST'])
def article_count():
    if request.method == "POST":
        id = request.form.get("id")
        try:
            cursor.execute("update favorite set count=count+1 where id=" + str(id))
            db.commit()
            print("count successfully!")
            return "1"
        except Exception as e:
            print("count failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


@app.route('/article/like', methods=['POST'])
def article_like():
    if request.method == "POST":
        uid = request.form.get("uid")
        aid = request.form.get("aid")
        try:
            cursor.execute("insert into LIKES(U_ID, A_ID) values (\""
                           + str(uid) + "\",\""
                           + str(aid) + "\")")
            cursor.execute("update article set LIKE_CNT = LIKE_CNT + 1 where A_ID =" + str(aid))
            db.commit()  # 提交，使操作生效
            print("add a new like successfully!")
            return "1"
        except Exception as e:
            print("add a new like failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


@app.route('/article/favorite', methods=['POST'])
def article_favorite():
    if request.method == "POST":
        uid = request.form.get("uid")
        aid = request.form.get("aid")
        try:
            cursor.execute("insert into favorite(U_ID, A_ID) values (\""
                           + str(uid) + "\",\""
                           + str(aid) + "\")")
            cursor.execute("update article set FAVORITE_CNT = FAVORITE_CNT + 1 where A_ID =" + str(aid))
            db.commit()  # 提交，使操作生效
            print("add a new favorite successfully!")
            return "1"
        except Exception as e:
            print("add a new like failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


@app.route('/favorite/list', methods=['POST'])
def favorite_list():
    if request.method == "POST":
        uid = request.form.get("uid")
        print(uid)
        cursor.execute(
            "select  favorite.A_ID, U_NAME,A_CONTENT,A_TIME, LIKE_CNT, FAVORITE_CNT, COMMENT_CNT, F_TIME from  user, article, favorite " +
            "where favorite.U_ID=" + str(
                uid) + " and user.U_ID=favorite.U_ID and article.A_ID = favorite.A_ID order by A_TIME desc")
        # cursor.execute("select  favorite.A_ID, U_NAME,A_CONTENT,A_TIME, LIKE_CNT from  user, article, favorite " +
        #                "where favorite.U_ID=4 and user.U_ID=favorite.U_ID and article.A_ID = favorite.A_ID order by A_TIME desc")
        data = cursor.fetchall()
        temp = {}
        result = []
        if (data != None):
            for i in data:
                temp["id"] = i[0]
                temp["wname"] = i[1]
                temp["content"] = i[2]
                temp["ctime"] = i[3]
                temp["like_cnt"] = i[4]
                temp['favorite_cnt'] = i[5]
                temp['comment_cnt'] = i[6]
                temp['favorite_time'] = i[7]
                result.append(temp.copy())  # 特别注意要用copy，否则只是内存的引用
            print("result:", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])


@app.route('/article/transmit', methods=['POST'])
def article_transmit():
    if request.method == "POST":
        uid = request.form.get("uid")
        aid = request.form.get("aid")
        cursor.execute("select TRANSMIT_ID, A_CONTENT from article where A_ID=" + str(aid))
        data = cursor.fetchone()
        print('data:' + str(data[0]))

        if data[0] != 0:
            origin_id = data[0]
        else:
            origin_id = aid
        print(aid, origin_id)
        try:
            cursor.execute("insert into transmit(U_ID, ORIGIN_A_ID) values (\""
                           + str(uid) + "\",\""
                           + str(origin_id) + "\")")
            cursor.execute("insert into article(U_ID, A_CONTENT, TRANSMIT_ID) values (\""
                           + str(uid) + "\",\""
                           + str(data[1]) + "\", \""
                           + str(origin_id) + "\")")
            db.commit()  # 提交，使操作生效
            print("add a new transmit successfully!")
            return "1"
        except Exception as e:
            print("add a new transmit failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


@app.route('/article/comment', methods=['POST'])
def comment_list():
    if request.method == "POST":
        aid = request.form.get("aid")
        print(aid)
        cursor.execute(
            "select  C_ID, U_NAME, C_CONTENT, C_TIME from user, comments " +
            "where comments.A_ID=" + str(aid) + " and user.U_ID=comments.U_ID")
        data = cursor.fetchall()
        temp = {}
        result = []
        if (data != None):
            for i in data:
                temp["id"] = i[0]
                temp["wname"] = i[1]
                temp["content"] = i[2]
                temp["ctime"] = i[3]
                result.append(temp.copy())  # 特别注意要用copy，否则只是内存的引用
            print("result:", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])


@app.route('/comment/add', methods=['POST'])
def comment_add():
    if request.method == "POST":
        uid = request.form.get("uid")
        aid = request.form.get("aid")
        content = request.form.get("content")
        try:
            cursor.execute("insert into comments(U_ID, A_ID, C_CONTENT) values (\""
                           + str(uid) + "\",\""
                           + str(aid) + "\",\""
                           + str(content) + "\")")
            cursor.execute("update article set COMMENT_CNT = COMMENT_CNT + 1 where A_ID =" + str(aid))
            db.commit()  # 提交，使操作生效
            print("add a new comment successfully!")
            return "1"
        except Exception as e:
            print("add a new comment failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


@app.route('/user/list', methods=['POST'])
def user_list():
    if request.method == "POST":
        uid = request.form.get("uid")
        print('uid:' + str(uid))
        cursor.execute("select U_ID,U_NAME from user where U_ID <> " + str(uid))
        data = cursor.fetchall()
        temp = {}
        result = []
        if (data != None):
            for i in data:
                temp["id"] = i[0]
                temp["wname"] = i[1]
                result.append(temp.copy())  # 特别注意要用copy，否则只是内存的引用
            print("result:", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])


@app.route('/follow/add', methods=['POST'])
def follow_add():
    if request.method == "POST":
        uid = request.form.get("uid")
        follow_id = request.form.get("follow_id")
        try:
            cursor.execute("insert into concern(CONCERN_U_ID, CONCERNED_U_ID) values (\""
                           + str(uid) + "\",\""
                           + str(follow_id) + "\")")
            db.commit()  # 提交，使操作生效
            print("add a new follow successfully!")
            return "1"
        except Exception as e:
            print("add a new follow failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


@app.route('/private_msg/add', methods=['POST'])
def private_msg_add():
    if request.method == "POST":
        uid = 0
        uid = request.form.get("uid")
        receiver_id = request.form.get("receiver_id")
        content = request.form.get("content")
        print(uid, receiver_id, content)
        try:
            cursor.execute("insert into private_message(SENDER_U_ID, RECEIVER_U_ID, MSG_CONTENT) values (\""
                           + str(uid) + "\",\""
                           + str(receiver_id) + "\",\""
                           + str(content) + "\")")
            db.commit()  # 提交，使操作生效
            print("add a new msg successfully!")
            return "1"
        except Exception as e:
            print("add a new msg failed:", e)
            db.rollback()  # 发生错误就回滚
            return "-1"


@app.route('/private_msg/list', methods=['POST'])
def private_msg_list():
    if request.method == "POST":
        uid = request.form.get("uid")
        print('uid:' + str(uid))

        cursor.execute("select  u1.U_NAME, u2.U_NAME, MSG_CONTENT, MSG_TIME from user u1, user u2, private_message "
                       + "where u1.U_ID=SENDER_U_ID and u2.U_ID=RECEIVER_U_ID and RECEIVER_U_ID=" + str(uid) + " order by MSG_TIME desc")
        data = cursor.fetchall()
        temp = {}
        result = []
        if (data != None):
            for i in data:
                temp["sender_name"] = i[0]
                temp["receiver_name"] = i[1]
                temp["content"] = i[2]
                temp["ctime"] = i[3]
                result.append(temp.copy())  # 特别注意要用copy，否则只是内存的引用
            print("result:", len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9090)
    db.close()
    print("Good bye!")
