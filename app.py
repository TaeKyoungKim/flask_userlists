from flask import Flask , render_template
from data import Articles
import pymysql


db = pymysql.connect(
            host='localhost', 
            user='root', 
            password='1234',
            db='gangnam',
            charset='utf8mb4')

cur = db.cursor()

app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET' , 'POST'])
def hello_world():
    return render_template('home.html' , name="김태경")

@app.route('/about', methods=['GET' , 'POST'])
def about():
    return render_template("about.html")

@app.route('/articles', methods=['GET' , 'POST'])
def articles():
    articles = Articles()
    query = 'SELECT * FROM topic;'

    cur.execute(query)

    db.commit()

    data = cur.fetchall()

    print(data[0][2])
    return render_template("articles.html" , articles = articles )

@app.route('/article/<id>', methods=['GET' , 'POST'])
def article(id):
    articles = Articles()
    print(len(articles))
    if len(articles)>=int(id):
        article = articles[int(id)-1]
        return render_template('article.html', article = article)
    else:
        return render_template('article.html', article = "NO DATA")

@app.route('/add_article', methods=['GET' , 'POST'])
def add_article():
    return render_template("add_article.html")

if __name__ == '__main__':
    app.run(port=5000)