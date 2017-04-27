# This is a test python file.
# Please do not touch unless your are ABSOLUTELY SURE ABOUT WHAT YOU ARE DOING
# Thanks :)

from flask import *

app = Flask(__name__)

# All app.route functions --------------#
@app.route('/')
def home():
    resp = make_response(render_template('index.html'))
    return resp

@app.route('/loginuser', methods=['POST'])
def calcmessage():
    # The script that runs once you login
    try:
        username = request.form['username']
        password = request.form['password']
    except:
        return redirect(url_for('home'))

    if username == 'james' and password == 'neverguess':
        print("Logging into james")
        resp = make_response(redirect(url_for('user')))
        print("Saved cookie 'currentUser'")
        resp.set_cookie('currentUser', 'james')
        return resp
    return redirect(url_for('home'))

@app.route('/user/')
def user():
    #Check that the user has permission
    try:
        cookie = request.cookies.get('currentUser')
        print('Username: ', cookie)
    except:
        print('No such cookie')
        return redirect(url_for('home'))

    if cookie == 'james':
        print('Found cookie and identified it as "james"')

        print("Rendering html..")
        #Since the request is legit we can extend the cookie expiration time
        resp = make_response(render_template('finances.html'))
        resp.set_cookie('currentUser', 'james')
        return resp
    return redirect(url_for('home'))




if __name__ == "__main__":
    # app.run(debug=True)
    app.run()
    #app.run('0.0.0.0', 8080)
