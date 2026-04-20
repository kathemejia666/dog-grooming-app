# Dog Grooming App

Aplicación web desarrollada con **Flask** y **MySQL** para gestionar citas de baño canino.  
Permite crear, listar, editar y eliminar citas desde una interfaz web sencilla.

## Características

- Crear nuevas citas
- Ver todas las citas registradas
- Editar citas existentes
- Eliminar citas
- Interfaz web simple y amigable
- Conexión a base de datos MySQL
- Despliegue probado en AWS EC2
- Respaldo de base de datos exportado y almacenado en Amazon S3

---

## Tecnologías usadas

- Python 3
- Flask
- MySQL
- mysql-connector-python
- Gunicorn
- HTML
- CSS
- AWS EC2
- Amazon S3

---

## Estructura del proyecto

```bash
dog-grooming-app/
├── app.py
├── requirements.txt
├── static/
│   └── style.css
└── templates/
    ├── index.html
    └── edit.html
```

---

## Funcionamiento del proyecto

La aplicación muestra una página principal donde el usuario puede registrar una cita ingresando:

- nombre del dueño
- nombre del perro
- fecha
- hora

Las citas quedan almacenadas en una tabla llamada `appointments` dentro de la base de datos `dog_grooming`.

Además, la aplicación permite:

- ver todas las citas agendadas
- editar una cita ya existente
- eliminar una cita

---

## Base de datos

Nombre de la base de datos:

```sql
dog_grooming
```

Tabla principal:

```sql
appointments
```

Estructura:

```sql
CREATE TABLE appointments (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) DEFAULT NULL,
  dog_name VARCHAR(100) DEFAULT NULL,
  date DATE DEFAULT NULL,
  time TIME DEFAULT NULL,
  PRIMARY KEY (id)
);
```

Ejemplo de datos:

```sql
INSERT INTO appointments VALUES
(1,'Tribilin','Paco','2026-04-21','10:00:00'),
(2,'Laura','Luna','2026-04-21','11:30:00'),
(3,'Carlos','Rocky','2026-04-22','09:15:00');
```

---

## Rutas principales de la aplicación

### `GET /`
Muestra todas las citas registradas.

### `POST /book`
Crea una nueva cita.

### `GET /edit/<id>`
Muestra el formulario para editar una cita.

### `POST /update/<id>`
Actualiza una cita existente.

### `GET /delete/<id>`
Elimina una cita.

---

## Cómo ejecutar el proyecto desde cero en una máquina local

### 1. Clonar el repositorio

```bash
git clone https://github.com/kathemejia666/dog-grooming-app.git
cd dog-grooming-app
```

### 2. Crear y activar entorno virtual

#### En Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### En Linux o macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

### 4. Crear la base de datos en MySQL

Entrar a MySQL:

```bash
mysql -u root -p
```

Luego ejecutar:

```sql
CREATE DATABASE dog_grooming;
USE dog_grooming;

CREATE TABLE appointments (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) DEFAULT NULL,
  dog_name VARCHAR(100) DEFAULT NULL,
  date DATE DEFAULT NULL,
  time TIME DEFAULT NULL,
  PRIMARY KEY (id)
);
```

Si quieres agregar datos de prueba:

```sql
INSERT INTO appointments (name, dog_name, date, time)
VALUES
('Tribilin', 'Paco', '2026-04-21', '10:00:00'),
('Laura', 'Luna', '2026-04-21', '11:30:00'),
('Carlos', 'Rocky', '2026-04-22', '09:15:00');
```

---

### 5. Configurar variables de entorno

La aplicación usa estas variables de entorno para conectarse a MySQL:

- `DB_HOST`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`

#### En Windows PowerShell

```powershell
$env:DB_HOST="localhost"
$env:DB_USER="grooming_app"
$env:DB_PASSWORD="TuPasswordSegura123!"
$env:DB_NAME="dog_grooming"
```

#### En Linux o macOS

```bash
export DB_HOST=localhost
export DB_USER=grooming_app
export DB_PASSWORD='TuPasswordSegura123!'
export DB_NAME=dog_grooming
```

> Si no tienes creado el usuario `grooming_app`, puedes usar temporalmente tu usuario de MySQL o crearlo manualmente.

Ejemplo para crearlo en MySQL:

```sql
CREATE USER 'grooming_app'@'localhost' IDENTIFIED BY 'TuPasswordSegura123!';
GRANT ALL PRIVILEGES ON dog_grooming.* TO 'grooming_app'@'localhost';
FLUSH PRIVILEGES;
```

Si ya existe:

```sql
ALTER USER 'grooming_app'@'localhost' IDENTIFIED BY 'TuPasswordSegura123!';
GRANT ALL PRIVILEGES ON dog_grooming.* TO 'grooming_app'@'localhost';
FLUSH PRIVILEGES;
```

---

### 6. Ejecutar la aplicación

```bash
python app.py
```

La aplicación quedará disponible normalmente en:

```text
http://127.0.0.1:5000
```

o

```text
http://localhost:5000
```

---

## Despliegue realizado en AWS

Este proyecto fue probado en:

- **AWS EC2** para ejecutar la aplicación Flask
- **MySQL** dentro de la instancia
- **Amazon S3** para almacenar un respaldo de la base de datos exportada en `.sql`

### Nota importante
En el entorno de AWS Academy no fue posible conectar EC2 a S3 mediante un rol IAM creado manualmente, porque el laboratorio no tenía permisos para crear roles. Por eso, el respaldo de la base de datos se generó en la instancia y luego se cargó manualmente al bucket S3.

---

## Exportar respaldo de la base de datos

Para generar un backup:

```bash
sudo mysqldump dog_grooming > dog_grooming.sql
```

Ese archivo puede subirse luego a Amazon S3 o guardarse como respaldo local.

---

## Posibles mejoras futuras

- Despliegue con Gunicorn y Nginx
- Persistencia automática al iniciar el servidor
- Subida automática de backups a S3
- Validaciones adicionales de formularios
- Mejoras visuales en la interfaz
- Uso de RDS en lugar de MySQL local en EC2

---

## Autor

Proyecto académico desarrollado para demostrar:

- desarrollo web con Flask
- integración con MySQL
- despliegue básico en AWS EC2
- uso de Amazon S3 para respaldos
