# Laboratorio de Jenkins
La práctica se va a enmarcarse en el contexto de un entorno de desarrollo de software. El punto de partida serán dos máquinas, una desde la que se desarrolla un proyecto de Python (dev-server) y otra donde se despliegan las versiones estables del mismo (pro-server). Durante la práctica, se añadirá un servidor con Jenkins encargado de cumplir los siguientes objetivos:
* Cada vez que se haga un commit en el proyecto se deberán correr los tests.
* Cuando se haga un commit sobre main, se subirá la versión al servidor de producción.

Para ello, aprenderemos a:
* Instalar y configurar un servidor de Jenkins.
* Definir un pipeline a través de un Jenkinsfile.
* Instalar plugins.
* Ejecutar código a través de ssh.

## Instalación de Jenkins
1. Clonarse el repositorio en nuestra máquina.
2. Ejecutar el docker-compose.yml. Para ello ejecutar `docker compose up -d` (o `docker-compose up -d` para versiones antiguas de Docker).
3. Entrar en la página de jenkins y seguir la instalación:
   1. Accedemos a la url http://localhost:8080/.
   2. Al comenzar nos pedirá un token. Lo encontraremos en los logs del contenedor. Para acceder, ejecutamos `docker logs jenkins`.
   3. Seleccionamos la instalación con los plugins por defecto "Install suggested plugins".
   4. Añadimos los datos que nos pide.

## Configuración del proyecto en GitHub
Crearemos un repositorio propio en GitHub para poder subir nuestro proyecto de Python. Además, configuraremos un token que nos permita hacer commits al repositorio.
1. Entramos en la sección de los repositorios y creamos uno nuevo. Añadimos la información necesaria.
2. Creamos un “Personal access token” de nuestra cuenta de github. Para ello seguimos los siguientes pasos:
   1. Vamos a la sección de settings.
   1. En el menú lateral, vamos a la última opción “Developer settings”.
   1. Seleccionamos Personal access tokens.
   1. Generamos uno nuevo con todos los permisos.
   1. Copiamos el token generado y lo guardamos a buen recaudo, ya que lo usaremos más adelante. Este token se usará de ahora en adelante como la contraseña.

## Configuración la tarea base de Jenkins
1. Clickamos en Nueva Tarea.
2. Le damos un nombre (suele ser buena idea darle el mismo nombre que el proyecto), seleccionamos multibranch pipeline y le damos a OK.
3. Le damos a Add source:
   1. Seleccionamos git.
   2. En el repositorio seleccionamos nuestro proyecto de GitHub.
   3. Como el proyecto es público, no nos hace falta introducir nuestras credenciales. Si no, deberíamos añadir usuario y el token como contraseña.
   4. Añadimos dos Behaviours para estar más seguros de que no ocurren errores inesperados en el futuro:
      * Clean after checkout.
      * Clean before checkout.
   5. Por último, seleccionamos la opción "Scan Multibranch Pipeline Triggers". Para el ejercicio, es mejor añadir un tiempo corto para reducir las esperas, como un minuto. En un ejemplo real, este número puede ser más alto.
   6. Guardamos.


## Iniciamos el proyecto de Python
Commitearemos el código base desde el servidor de desarrollo.
1. Accedemos al servidor de desarrollo con el comando `docker exec -it dev-server bash`.
2. Configuramos nuestros credenciales de git. Para ello, ejecutamos los siguientes comandos:
```shell
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```
3. Subimos el código a nuestro repositorio con los comandos añadidos a continuación. Cuando nos pida la contraseña, deberemos introducir el token.
```shell
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin <url del proyecto>
git push origin main
```

## Configuración de los tests en Jenkins
Añadiremos al proyecto el `Jenkinsfile` que ejecuta los tests automáticos:
1. En el entorno de desarrollo, en la carpeta del proyecto, creamos un fichero llamado `Jenkinsfile` con el siguiente contenido:
```shell
pipeline {
  agent any
  stages {
    stage('Test') {
      steps {
        sh 'python3 test.py'
      }
    }
  }
}
```
2. Lo subimos a GitHub:
```shell
git add .
git commit -m "Añadido el Jenkinsfile con la configuración de los tests automáticos."
git push origin main
```

## Configuración del servidor de producción
Nos bajaremos la versión actual del proyecto y dejaremos preparado el script que realiza el despliegue.
1. Accedemos al servidor a través de ssh con el comando `ssh test@localhost`. La contraseña es `test`.
2. Accedemos al directorio donde queremos desplegar el proyecto. Por ejemplo, `/opt`. Para ello, ejecutamos el comando `cd /opt`.
3. Nos bajamos el proyecto por primera vez ejecutando el comando `git clone <url del proyecto>`.
4. Ejecutamos el script `main.py` para comprobar el funcionamiento de la versión inicial.
5. En el home del usuario, `/home/ubuntu/`, añadimos el script `deploy.sh` encargado de desplegar la aplicación las siguientes veces:
```shell
#!/bin/bash
cd /opt/<nombre del repositorio>
git pull origin main
```
6. Le asignamos permisos de ejecución con el comando `chmod +x deploy.sh`.

## Configuración del despliegue desde Jenkins
Modificaremos el `Jenkinsfile` para que despliegue la aplicación cuando se commitee algo en main. Por último, comprobaremos el flujo completo del pipeline realizando una modificación en el proyecto de Python.
1. Añadimos en jenkins el plugin "SSH Pipeline Steps". Para ello:
   1. Accedemos a la sección "Administrar Jenkins".
   2. Accedemos a "Administrar Plugins".
   3. Buscamos el plugin "SSH Pipeline Steps" y lo instalamos.
2. Accedemos al servidor de desarrollo.
3. Añadimos un nuevo stage que solo se ejecutará en la rama main y que se conectará por ssh al servidor de producción para hacer el despliegue. Además, añadimos una variable en jenkins con la información del servidor. El resultado del Jenkinsfile es el siguiente:
```shell
def remote = [:]
remote.name = 'test'
remote.host = 'pro-server'
remote.user = 'test'
remote.password = 'test'
remote.allowAnyHosts = true

pipeline {
  agent any
  stages {
    stage('Test') {
      steps {
        sh 'python3 test.py'
      }
    }
    stage('Deploy') {
      when {
        branch 'main'
      }
      steps {
        sshCommand remote: remote, command: "./deploy.sh"
      }
    }
  }
}
```
4. Subimos los cambios a GitHub.
5. Creamos una nueva rama de desarrollo en la que modificaremos el fichero. Para ello, ejecutamos `git checkout -b dev`.
6. Añadimos ciertos cambios a la calculadora. Por ejemplo, la multiplicación.
7. Commiteamos y pusheamos los cambios. Vemos que solo se ejecutan los tests.
8. Mergeamos los cambios en main. Para ello, ejecutamos los siguientes comandos:
```shell
git checkout main
git merge dev
git push origin main
```
9. Accedemos al servidor de producción para comprobar que se han subido los cambios.
