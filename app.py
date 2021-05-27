from flask import Flask , render_template

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
    return render_template("articles.html")
if __name__ == '__main__':
    app.run(port=5000)