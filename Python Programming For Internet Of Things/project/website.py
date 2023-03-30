import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


def database_conn(sql_statement):
    #  try:
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute(sql_statement)
    out = cursor.fetchall()  #returns a list
    cursor.close()
    conn.commit()
    conn.close()
    return out
    #  except:
    #    print("Error")


@app.route('/class')
def _class():
    classes = database_conn("select name from class;")
    return render_template('class.html', classes=classes)


@app.route('/class/<classid>')
def lesson(classid):
    dates = database_conn(
        f"select lessonid, date from lesson where classid={classid};")
    return render_template('lesson.html', dates=dates)


@app.route('/lesson/<lessonid>')
def attendance(lessonid):
    students = database_conn(
        f"select firstname, lastname, uid, present from students inner join enrollment on enrollment.studentid=students.studentid inner join attendance on attendance.studentid=students.studentid where enrollment.classid=(select classid from lesson where lessonid={lessonid}) and lessonid={lessonid};"
    )
    return render_template('attendance.html',
                           students=students,
                           lessonid=lessonid)


@app.route('/attendance/<lessonid>', methods=['POST'])
def updateAttendance(lessonid):
  students = database_conn(f"select students.studentid from students inner join enrollment on enrollment.studentid=students.studentid inner join attendance on attendance.studentid=students.studentid where enrollment.classid=(select classid from lesson where lessonid={lessonid}) and lessonid={lessonid};")
  for ((key, value),studentid) in zip(request.form.items(), students):
    database_conn(f"update attendance set present='{value[0]}' where studentid={studentid[0]};")
  return redirect(f"/lesson/{lessonid}", code=302)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
