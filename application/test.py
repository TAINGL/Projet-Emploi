from flask import request, redirect

app = Flask(__name__)

@app.route('/search', methods = ['POST'])
def search():
    email = request.form['email']
    print("The email address is '" + email + "'")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)