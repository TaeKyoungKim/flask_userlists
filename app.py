from flask import Flask , render_template , redirect ,request
from data import Articles
import pymysql
from passlib.hash import sha256_crypt

db = pymysql.connect(
            host='localhost', 
            user='root', 
            password='1234',
            db='gangnam',
            charset='utf8mb4')

cur = db.cursor()

app = Flask(__name__)
app.debug = True

@app.route('/register', methods=['GET','POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    password_1 = sha256_crypt.encrypt("1234")
    print(password_1)
    print(sha256_crypt.verify("1234", password_1))
    
    return "SUCCESS"


@app.route('/', methods=['GET' , 'POST'])
def hello_world():
    return render_template('home.html' , name="김태경")

@app.route('/about', methods=['GET' , 'POST'])
def about():
    return render_template("about.html")

@app.route('/articles', methods=['GET' , 'POST'])
def articles():
    # articles = Articles()
    query = 'SELECT * FROM topic;'

    cur.execute(query)

    db.commit()

    articles = cur.fetchall()

    print(articles)
    return render_template("articles.html" , articles = articles )

@app.route('/article/<id>', methods=['GET' , 'POST'])
def article(id):
    # articles = Articles()
    # print(len(articles))
    # if len(articles)>=int(id):
    #     article = articles[int(id)-1]
    #     return render_template('article.html', article = article)
    # else:
    #     return render_template('article.html', article = "NO DATA")
    query = f'SELECT * FROM topic WHERE id = {id}'
    
    cur.execute(query)

    db.commit()

    article  = cur.fetchone()
    print(article)
    if article ==None:
        return redirect('/articles')
    else:
        return render_template('article.html',article = article )


@app.route('/article/<id>/delete', methods=['GET' , 'POST'])
def delete_article(id):
    query = f'DELETE FROM `gangnam`.`topic` WHERE id={id}'
    cur.execute(query)

    db.commit()

    return redirect('/articles')

@app.route('/add_article' , methods=['GET','POST'])
def add_articles():

    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        author = request.form['author']
        
        print(title, description, author) 
        
        # query = f'INSERT INTO `topic` (`title`, `description`, `author`) VALUES ({title}, {description}, {author});'
        
        # cur.execute(query)
        # db.commit()
        query = "INSERT INTO `topic` (`title`, `description`, `author`) VALUES (%s, %s, %s);"
        input_data = [title,description,author ]
        # print(request.form['desc'])

        cur.execute(query, input_data)
        db.commit()
        print(cur.rowcount)
        # db.close()
        return redirect("/articles")
    else:
        return render_template('add_article.html')

@app.route("/article/<id>/edit", methods=['GET', 'POST'])
def edit_article(id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        author = request.form['author']
        # print(title, description, author)
        # return "SUCCESS"
        query = f"UPDATE topic SET  title='{title}',description= '{description}' ,author='{author}' WHERE id = {id};"
        print(query)
        cur.execute(query)

        db.commit()

        return redirect('/articles')
        
    else:
        query = f"SELECT * FROM topic WHERE id = {id};"

        cur.execute(query)
        db.commit()

        article = cur.fetchone()

        return render_template('edit_article.html' , article = article)


if __name__ == '__main__':
    app.run(port=5000)