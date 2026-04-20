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
- Exposición pública por puerto 80 usando **Nginx**
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
- Nginx
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

# Ejecución local desde cero

## 1. Clonar el repositorio

```bash
git clone https://github.com/kathemejia666/dog-grooming-app.git
cd dog-grooming-app
```

## 2. Crear y activar entorno virtual

### En Windows

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### En Linux o macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 4. Crear la base de datos en MySQL

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

## 5. Configurar variables de entorno

La aplicación usa estas variables de entorno para conectarse a MySQL:

- `DB_HOST`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`

### En Windows PowerShell

```powershell
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASSWORD="TU_PASSWORD"
$env:DB_NAME="dog_grooming"
```

### En Linux o macOS

```bash
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD='TU_PASSWORD'
export DB_NAME=dog_grooming
```

> También puedes crear un usuario específico como `grooming_app` y usarlo en vez de `root`.

Ejemplo:

```sql
CREATE USER 'grooming_app'@'localhost' IDENTIFIED BY 'TuPasswordSegura123!';
GRANT ALL PRIVILEGES ON dog_grooming.* TO 'grooming_app'@'localhost';
FLUSH PRIVILEGES;
```

## 6. Ejecutar la aplicación

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

# Despliegue en AWS EC2 paso a paso

Esta sección describe cómo conectarse a la instancia **EC2** y dejar la aplicación disponible públicamente.

## 1. Requisitos previos

Necesitas tener:

- una instancia EC2 Ubuntu en ejecución
- la IP pública de la instancia
- el archivo `.pem` de acceso SSH
- el puerto **22** abierto para SSH
- el puerto **80** abierto para HTTP
- opcionalmente el puerto **5000** abierto si quieres probar Flask directamente

## 2. Conectarse a la instancia EC2

Desde PowerShell o terminal local:

```powershell
ssh -i "C:\ruta\a\mi-clave.pem" ubuntu@18.234.170.99
```

Si entra correctamente, verás algo así:

```bash
ubuntu@ip-172-31-22-21:~$
```

## 3. Ir al proyecto dentro del servidor

```bash
cd ~/dog-grooming-app
```

Si todavía no existe, puedes clonar el repositorio:

```bash
git clone https://github.com/kathemejia666/dog-grooming-app.git
cd dog-grooming-app
```

## 4. Crear entorno virtual e instalar dependencias en EC2

```bash
sudo apt update
sudo apt install python3-pip python3-venv -y
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 5. Configurar MySQL en EC2

Entrar a MySQL con permisos de administrador:

```bash
sudo mysql
```

Crear o ajustar el usuario de la aplicación:

```sql
CREATE USER IF NOT EXISTS 'grooming_app'@'localhost' IDENTIFIED BY 'TuPasswordSegura123!';
ALTER USER 'grooming_app'@'localhost' IDENTIFIED BY 'TuPasswordSegura123!';
GRANT ALL PRIVILEGES ON dog_grooming.* TO 'grooming_app'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## 6. Exportar variables de entorno en EC2

```bash
export DB_HOST=localhost
export DB_USER=grooming_app
export DB_PASSWORD='TuPasswordSegura123!'
export DB_NAME=dog_grooming
```

## 7. Levantar la aplicación Flask en EC2

Antes de ejecutar la app, si el puerto 5000 quedó ocupado por un proceso anterior:

```bash
sudo fuser -k 5000/tcp
```

Luego ejecutar:

```bash
python3 app.py
```

Si todo está bien, Flask quedará escuchando en el puerto 5000.

Prueba directa:

```text
http://18.234.170.99:5000
```

---

# Exponer la app en el puerto 80 con Nginx

Para que la aplicación abra directamente con:

```text
http://18.234.170.99
```

se configuró **Nginx** como proxy desde el puerto 80 hacia Flask en el puerto 5000.

## 1. Instalar Nginx en EC2

```bash
sudo apt update
sudo apt install nginx -y
```

## 2. Crear la configuración del sitio

```bash
sudo nano /etc/nginx/sites-available/dog-grooming
```

Contenido:

```nginx
server {
    listen 80;
    server_name 18.234.170.99;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 3. Activar la configuración

```bash
sudo ln -s /etc/nginx/sites-available/dog-grooming /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 4. Abrir el puerto 80 en el Security Group

En AWS EC2, en el **Security Group** de la instancia, agregar una regla de entrada:

- Tipo: **HTTP**
- Puerto: **80**
- Origen: `0.0.0.0/0` o el rango permitido que se necesite

## 5. Acceso final

Una vez configurado Nginx, cualquier persona con acceso a internet puede abrir:

```text
http://18.234.170.99
```

> No necesita instalar Python, MySQL ni entrar por SSH. Solo abrir la URL.

---

# Respaldo en Amazon S3

Este proyecto también fue probado con almacenamiento de respaldo en S3.

## Crear respaldo SQL desde EC2

```bash
sudo mysqldump dog_grooming > dog_grooming.sql
```

## Subir el archivo al bucket S3

En este proyecto se utilizó un bucket como respaldo:

```text
dog-grooming-backups-kathe-2026
```

Debido a restricciones de AWS Academy, no fue posible crear un rol IAM para que EC2 subiera automáticamente a S3. Por eso, el archivo `.sql` se generó en la instancia y luego se cargó manualmente al bucket S3.

---

## Qué debe hacer otra persona para usar la app desde otro PC o red

Si la instancia ya está encendida, Nginx está configurado y la aplicación Flask está corriendo en EC2, la otra persona solo debe abrir:

```text
http://18.234.170.99
```

No necesita:

- clonar el repositorio
- instalar Python
- instalar MySQL
- conectarse por SSH
- ejecutar comandos

---

## Limitación actual

Actualmente la aplicación sigue levantándose manualmente con:

```bash
python3 app.py
```

Eso significa que si el proceso se detiene o la terminal se cierra, habrá que volver a entrar a EC2 y ejecutarla de nuevo.

## Mejora recomendada futura

Para que la app quede siempre activa sin necesidad de abrir terminal manualmente, se recomienda después configurar:

- **Gunicorn**
- **systemd**
- **Nginx** como proxy permanente

---

## Posibles mejoras futuras

- Persistencia automática al iniciar el servidor
- Subida automática de backups a S3
- Validaciones adicionales de formularios
- Mejoras visuales en la interfaz
- Uso de RDS en lugar de MySQL local en EC2
- Dominio propio y HTTPS

---

## Autor

Proyecto académico desarrollado para demostrar:

- desarrollo web con Flask
- integración con MySQL
- despliegue en AWS EC2
- exposición pública mediante Nginx
- uso de Amazon S3 para respaldos
