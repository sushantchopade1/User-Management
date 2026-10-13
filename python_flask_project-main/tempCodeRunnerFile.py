from flask import Flask

app = Flask(__name__)

@app.route("/")  #decorator
def hello():
    return "<h1>Hello, World!asdfsda</h1>"

@app.route("/home")  #decorator
def home():
    return f"<h1>Home!</h1>"

@app.route("/home/<para>")  #decorator
def home(para):
    return f"<h1>Home!{para}</h1>"

@app.route("/about/<username>")  #decorator
def about(username):
    return f'<h1>this is about {username} and klasdf</h1>'


if __name__ == '__main__': 
 app.run(port=8000, debug=True)