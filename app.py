from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# 👉 CONEXIÓN A MYSQL (AJUSTA TU PASSWORD)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",  # 👈 CAMBIA ESTO
    database="dog_grooming"
)

cursor = db.cursor(dictionary=True)


# 👉 VER TODAS LAS CITAS
@app.route('/')
def index():
    cursor.execute("SELECT * FROM appointments")
    appointments = cursor.fetchall()
    return render_template('index.html', appointments=appointments)


# 👉 CREAR CITA
@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    dog_name = request.form['dog_name']
    date = request.form['date']
    time = request.form['time']

    sql = "INSERT INTO appointments (name, dog_name, date, time) VALUES (%s, %s, %s, %s)"
    values = (name, dog_name, date, time)

    cursor.execute(sql, values)
    db.commit()

    return redirect(url_for('index'))


# 👉 ELIMINAR CITA
@app.route('/delete/<int:id>')
def delete(id):
    cursor.execute("DELETE FROM appointments WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('index'))


# 👉 MOSTRAR FORMULARIO PARA EDITAR
@app.route('/edit/<int:id>')
def edit(id):
    cursor.execute("SELECT * FROM appointments WHERE id = %s", (id,))
    appointment = cursor.fetchone()

    if appointment is None:
        return "Cita no encontrada", 404

    return render_template('edit.html', appointment=appointment)


# 👉 ACTUALIZAR (REPROGRAMAR) CITA
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form['name']
    dog_name = request.form['dog_name']
    date = request.form['date']
    time = request.form['time']

    sql = """
    UPDATE appointments 
    SET name=%s, dog_name=%s, date=%s, time=%s 
    WHERE id=%s
    """
    values = (name, dog_name, date, time, id)

    cursor.execute(sql, values)
    db.commit()

    return redirect(url_for('index'))


# 👉 INICIAR SERVIDOR
if __name__ == '__main__':
    app.run(debug=True)