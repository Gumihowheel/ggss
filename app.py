from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# MySQL所在的主机名
HOSTNAME = "127.0.0.1"
# MySQL监听的端口号，默认3306
PORT = 3306
# 连接MySQL的用户名，读者用自己设置的
USERNAME = "root"
# 连接MySQL的密码，读者用自己的
PASSWORD = "root"
# MySQL上创建的数据库名称
DATABASE = "database_learn"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

# 在app.config中设置好连接数据库的信息，
# 然后使用SQLAlchemy(app)创建一个db对象
# SQLAlchemy会自动读取app.config中连接数据库的信息

db = SQLAlchemy(app)

migrate = Migrate(app, db)

# #测试数据库是否连接成功
# with app.app_context():
#     with db.engine.connect() as conn:
#         rs = conn.execute("select 1")
#         print(rs.fetchone())

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    #db.string最多存255
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    #添加作者的外键 (要跟user的id保持一致
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # 会使用上面的外键信息,将user的内容查询出来,放在author中
    #backref会自动给User模型添加一个articles属性,用来获取文章
    author = db.relationship("User",backref="articles")


# article = Article(title="Flask学习大纲", content="FlaskXXXXXXXXXXXXXXx")
# #article.author_id = user.id
# #user = User.query.get(article.author_id)




#可以这样用
#user = User(username="法外狂徒张三", password="111111")
#sql:insert user(username,password) values('法外狂徒张三'，'111111');

# #把所有数据库关系映射出去
# with app.app_context():
#     db.create_all()

@app.route("/user/add")
def app_user():
    # 1.创建ORM对象
    user = User(username='法外狂徒张三', password = '111111')
    # 2.将ORM对象添加到db.session中
    db.session.add(user)
    # 3.将db.session中的改变同步到数据空中
    db.session.commit()
    return "用户创建成功"

@app.route("/user/query")
def query_user():
    # #1.get 查找 根据主键查找
    # user = User.query.get(1)
    # #获得是一个user对象，我们可以使用user.id user.password 来调用里面的内容
    # print(user.password)

    #2.filter_by 查找
    users = User.query.filter_by(username = '法外狂徒张三')
    #获得是一个类数组对象
    for user in users:
        print(user.username,user.password)

    return "查找成功"

@app.route("/user/update")
def update_user():
    #如果这里使用切片0,[0],若没有查到数据可能会报错,可以考虑第二种写法,(此时返回的是User对象,不是query对象
    user = User.query.filter_by(username="法外狂徒张三")[0]
    #第二种写法,使用first函数,没有数据不会报错(此时返回的是User对象,不是query对象
    user = User.query.filter_by(username="法外狂徒张三").first()
    user.password = "2222222"
    #不需要add了
    db.session.commit()
    return "数据修改成功"

@app.route("/user/delete")
def delete_user():
    #1查找
    user = User.query.get(1)
    #2从 db.session中删除
    db.session.delete(user)
    #3 commit同步
    db.session.commit()
    return "删除成功"

@app.route("/article/add")
def article_add():
    article = Article(title="Falsk学习框架", content="FlaskXXXXXXX")
    article.author = User.query.get(2)

    article1 = Article(title="Falsk学习框架1111", content="FlaskXXXXXXX1111")
    article1.author = User.query.get(2)

    #添加到session中
    db.session.add_all([article,article1])
    #再同步到数据库上
    db.session.commit()
    return "文章添加成功"

@app.route("/article/query")
def query_article():
    user = User.query.get(2)
    for article in user.articles:
        print(article.title)
    return "文章查找成功"


if __name__ == '__main__':
    app.run(debug=True)
