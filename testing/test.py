from flask import *
app = Flask(__name__)

data = 'James'

@app.route('/')
def home():
    return render_template("test.html", data=data)


if __name__ == "__main__":
    app.run()
