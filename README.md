•	Manual de instalación
1.  Clonar el repositorio
•	Clonamos repositorio a nuestro equipo
•	
•	git clone https://github.com/RelatifVision/PrimeVideo.git
•	cd <<ruta/tu/repositorio>>

2.  Creamos y activamos Entorno Virtual
•	Crear Entorno Virtual
•	python -m venv env
•	Activar entorno Virtual
•	.\env\Scripts\Activate.ps1 # PowerShell
•	.\env\Scripts\Activate.ps1 # CMD
•	source env/bin/actívate # macOS/Linux

3.  Instalar las Dependencias
•	Instalar las dependencias listadas en el archivo ‘requirements.txt’
•	pip install -r requirements.txt

4.  Configurar variables de Entorno
•	Puedes hacerlo creando el archivo env en el directorio raíz del proyecto.
•	SECRET_KEY=<<tu_secret_key>>
•	DEBUG=True
•	DATABASE_URL=postgres://usuario:contraseña@localhost:5432/tu_base_de_datos

5.  Migrar la Base de Datos
•	Aplica las migraciones de la DDBB para asegurarte de que la estructura de la DDBB está actualizada.
•	python manage.py migrate
6.  Crear Superusuario (Opcional):
•	Si necesitas acceso de administrador, crea superusuario
•	python manage.py createsuperuser
•	
•	Si no, tienes estos user y pass que son admin:
o	admin    4dM1Ni57r@D0
o	javi95   2295
7.  Ejecutar el Servidor de Desarrollo:
•	Inicia el servidor de desarrollo para verificar que todo funcione correctamente.
•	python manage.py runserver

*8.  Configuración al Servidor de Producción (Opcional): *AT THE MOMENT ITS NOT PREPARE ONLY DEVELOPING
•	Asegúrate de configurar un servidor de producción como Gunicorn y un servidor web como Nginx.
•	
•	gunicorn tu_proyecto.wsgi:application --bind 0.0.0.0:8000
Ejemplo configuración Nginx
•	server {
•	    listen 80;
•	    server_name tu_dominio.com;
•	
•	    location / {
•	        proxy_pass http://127.0.0.1:8000;
•	        proxy_set_header Host $host;
•	        proxy_set_header X-Real-IP $remote_addr;
•	        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
•	        proxy_set_header X-Forwarded-Proto $scheme;
•	    }
•	
•	    location /static/ {
•	        alias /ruta/a/tu_proyecto/static/;
•	    }
•	
•	    location /media/ {
•	        alias /ruta/a/tu_proyecto/media/;
•	    }
•	}
