from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# flask --app flask_app run --debug

app = Flask(__name__)
connection = sqlite3.connect("pets.db",check_same_thread=False)

@app.route("/hello")
def hello():
    return "<p>Hello, World!</p>"

@app.route("/")
@app.route("/list")
def get_list():
    cursor = connection.cursor()
    results = cursor.execute("SELECT * FROM pets").fetchall()
    return render_template("list.html",results=results)
    # html = "<p><b>Here is your list:</b></p>\n<pre>"
    # for result in results:
    #     html += f"{result[0]}: {result[1]} is a {result[2]} who is {result[3]} years old\n"
    # html += "</pre>"
    # return html

@app.route("/create", methods=["GET","POST"])
def get_post_create():
    if request.method == "GET":
        return render_template("create.html")
    elif request.method == "POST":
        data = dict(request.form)
        data["age"] = float(data["age"]) if data["age"].isnumeric() else 0

        cursor = connection.cursor()
        cursor.execute("INSERT INTO pets (name, age, type, owner) VALUES (?,?,?,?)",(data['name'], data['age'], data['type'], data['owner'],))
        connection.commit()
        return redirect(url_for('get_list'))
    
@app.route("/update/<id>", methods=["GET"])
def get_update(id):
    cursor = connection.cursor()
    row = cursor.execute(f"SELECT * FROM pets WHERE id={id}").fetchall()[0]
    data = {'id':row[0],'name':row[1],'type':row[2],'age':float(row[3]),'owner':row[4]}
    print(data)
    return render_template("update.html",data=data)

@app.route("/update/<id>", methods=["POST"])
def post_update(id):
    data = dict(request.form)
    data["age"] = float(data["age"]) if data["age"].isnumeric() else 0

    cursor = connection.cursor()
    cursor.execute("UPDATE pets SET name = ?, age = ?, type = ?, owner = ? WHERE id=?",(data['name'], data['age'], data['type'], data['owner'],id))
    connection.commit()
    return redirect(url_for('get_list'))

    

@app.route("/goodbye")
def goodbye():
    return "<h1>Goodbye!</h1>"

@app.route("/delete/<id>")
def delete(id):
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM pets WHERE id={id}")
    return redirect(url_for('get_list'))

if __name__ == "__main__":
    app.run(debug=True)