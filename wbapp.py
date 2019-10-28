from flask import Flask, render_template

#instantiate the class
app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html",say_hi_name="Iulian")

#when the script is executed by running the command 
# 'python wbapp.py' the __name__ variable gets value __main__
if __name__=="__main__":
    app.run(debug=True)