# 初始化資料庫連線
import pymongo
client=pymongo.MongoClient("mongodb+srv://@mycluster.ogpqpks.mongodb.net/?retryWrites=true&w=majority")
db = client.member_system

from flask import *
app = Flask(__name__,static_folder="static",static_url_path="/")

app.secret_key="any string but secret"
# 連首頁
@app.route("/")
def index():
    return render_template("welcome.html")

# 錯誤畫面
@app.route("/error")
def error():
    message = request.args.get("msg","發生錯誤，請聯繫客服")
    return render_template("error.html",message=message)
# 首頁按註冊
@app.route("/member", methods=['GET', 'POST'])
def register():
    return render_template("member.html")
# 進註冊畫面擷取使用者輸入資料
@app.route("/sueccess",methods=["POST"])
def sueccess():
    name = request.form["name"]
    tel = request.form["tel"]
    email = request.form["email"]
    password = request.form["password"]
    collection=db.user
    # 檢查會員集合中是否有相同的 Email 的文件資料
    result = collection.find_one({
        "email":email
    })
    if result != None:
        return redirect("/error?msg=信箱已經被註冊")
    # 把資料放進資料庫，完成註冊
    collection.insert_one({
        "name":name,
        "tel":tel,
        "email":email,
        "password":password
    })
    return render_template("sueccess.html")

# 已有帳號登入確認
@app.route("/signin", methods=['GET', 'POST'])
def signin():
    email = request.form["email"]
    password = request.form["password"]
    collection = db.user
    result = collection.find_one({
        "$and":[
            {"email":email},
            {"password":password}
        ]
    })
    #找不到對應的資料，登入失敗，導向到錯誤頁面
    if result == None:
        return redirect("/error?msg=帳號或密碼輸入錯誤")
    #登入成功，導向到會員會面
    return render_template("menu.html",data=result["name"])
# 訂單選定後再確認訂單
@app.route('/check',methods=["POST"])
def order():
    ice = request.form["ice"]
    sweet = request.form['sweet']
    mix = ', '.join(request.form.getlist('mix'))
    receive = request.form['receive']
    beverage = request.form["beverage"]
    return render_template('order.html',beverage=beverage,ice=ice,sweet=sweet,mix=mix,receive=receive)

@app.route("/end",methods=["POST"])
def end():
    return render_template("end.html")

# 再次訂購
@app.route("/again")
def again():
    return render_template("menu.html")
# 登出
@app.route("/signout")
def signout():
    return render_template("welcome.html")
# 啟動伺服器
app.run(port=3000)
