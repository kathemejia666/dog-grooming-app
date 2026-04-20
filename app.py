from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "grooming_app"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "dog_grooming")
    )


# 👉 VER TODAS LAS CITAS
@app.route('/')
def index():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM appointments")
    appointments = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('index.html', appointments=appointments)


# 👉 CREAR CITA
@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    dog_name = request.form['dog_name']
    date = request.form['date']
    time = request.form['time']

    db = get_db_connection()
    cursor = db.cursor()

    sql = "INSERT INTO appointments (name, dog_name, date, time) VALUES (%s, %s, %s, %s)"
    values = (name, dog_name, date, time)

    cursor.execute(sql, values)
    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for('index'))


# 👉 ELIMINAR CITA
@app.route('/delete/<int:id>')
def delete(id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM appointments WHERE id = %s", (id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('index'))


# 👉 MOSTRAR FORMULARIO PARA EDITAR
@app.route('/edit/<int:id>')
def edit(id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM appointments WHERE id = %s", (id,))
    appointment = cursor.fetchone()
    cursor.close()
    db.close()

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

    db = get_db_connection()
    cursor = db.cursor()

    sql = """
    UPDATE appointments
    SET name=%s, dog_name=%s, date=%s, time=%s
    WHERE id=%s
    """
    values = (name, dog_name, date, time, id)

    cursor.execute(sql, values)
    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for('index'))


# 👉 INICIAR SERVIDOR
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)