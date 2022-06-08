import datetime
from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, init, upgrade, migrate as makemigrations
from datetime import timedelta



app = Flask(__name__, static_url_path="/static")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db1.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "e039ced5906470d690fe6ce3"
app.permanent_session_lifetime = timedelta(minutes=60)
db = SQLAlchemy(app)
migrate = Migrate(app, db)



#####################models#####################
class Article(db.Model):
    __tablename__ = 'blog_article'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(255))
    image = db.Column(db.String(255))
    content = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('blog_category.id'), nullable=True)

class Category(db.Model):
    __tablename__ = 'blog_category'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)



#####################routes#####################
@app.route("/")
def index():
    articles = Article.query.all()
    return render_template("index.html", articles=articles,)

@app.route("/article/<id>")
def article(id):
    article = Article.query.filter(Article.id==id).first()
    return render_template("article.html", article=article)
    
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/category", methods=['GET', 'POST'])
def categories():
    if request.method == 'POST':
        name = request.form.get('title')
        newcategory = Category(name=name)
        db.session.add(newcategory)
        db.session.commit()
        return redirect('/category')
    else: 
        categories = Category.query.order_by(Category.created_date.desc())
        result = []
        for item in categories:
            if item.name not in ["Sport"]:
                result.append(item)
        return render_template("category/index.html", categories=result)

@app.route("/category/<id>")
def category(id):
    category = Category.query.filter(Category.id==id).first()
    articles = Article.query.filter(Article.category_id==id)   
    return render_template("category/id.html", category=category, articles=articles)

@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		session.permanent = True
		user = request.form["nm"]
		session["user"] = user
		return redirect(url_for("user"))
	else:
		if "user" in session:
			return redirect(url_for("user"))

		return render_template("login.html")

@app.route("/user")
def user():
	if "user" in session:
		user = session["user"]
		return render_template("user.html", user=user)
	else:
		return redirect(url_for("login"))

@app.route("/logout")
def logout():
	session.pop("user", None)
	return redirect(url_for("login"))

@app.route("/update")
def update():
    return 0;


with app.app_context():
    db.create_all()
    # init()
    # makemigrations()
    # upgrade()

app.run(host="0.0.0.0", debug=True)
