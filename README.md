# Tutorial
La práctica va a consistir en crear una configuración de Jenkins que nos ayude a cumplir dos objetivos:
* Cada vez que se haga un commit en el proyecto se deberán correr los tests.
* Cuando se haga un commit sobre main, se subirá la versión al servidor de producción.

## Instalación:
1. Ejecutar el docker-compose.yml ya creado. (Una explicación aquí de los distintos contenedores y demás).
2. Entrar en la página de jenkins y seguir la instalación.
   1. Seleccionamos la instalación con los plugins por defecto "Install suggested plugins".
   2. Añadimos los datos que nos pide.

## Configuramos nuestro proyecto en github:
1. Entramos en la sección de los repositorios y creamos uno nuevo. Añadimos la información necesaria.
2. Clonamos el proyecto base con el comando “git clone https://github.com/oscar90y5/jenkins-base-project.git” (Aquí explicar el proyecto. Los ficheros que hay y para qué sirven).
3. Eliminamos la carpeta de .git con el comando `rm -rf .git`.
4. Creamos un “Personal access token” de nuestra cuenta de github. Para ello seguimos los siguientes pasos:
   1. Vamos a la sección de settings.
   1. En el menú lateral, vamos a la última opción “Developer settings”.
   1. Seleccionamos Personal access tokens.
   1. Generamos uno nuevo con todos los permisos.
   1. Copiamos el token generado y lo guardamos a buen recaudo, ya que lo usaremos más adelante. Este token se usará de ahora en adelante como la contraseña.
5. Configuramos nuestra cuenta en el servidor de desarrollo. Para ello, ejecutamos los siguientes comandos:
```shell
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```
6. Subimos el código a nuestro proyecto con los comandos añadidos a continuación. Cuando nos pida la contraseña deberemos introducir el token.
```shell
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin <url del proyecto>
git push origin main
```

## Configuramos el servidor de producción:
1. Accedemos al directorio donde queremos desplegar el proyecto. Por ejemplo, `/opt`. Para ello, ejecutamos el comando `cd /opt`.
2. Nos bajamos el proyecto por primera vez ejecutando el comando `git clone <url del proyecto>`.
3. En el home del usuario, añadimos el script 'deploy.sh' encargado de desplegar la aplicación las siguientes veces:
```shell
#!/bin/bash
cd /opt/<nombre del proyecto>
git pull origin main
```
3. Le asignamos permisos de ejecución con el comando `chmod +x deploy.sh`.
4. Ejecutamos el main.py para comprobar el funcionamiento de la versión inicial.

## Configurar la tarea base:
1. Clickamos en Nueva Tarea.
2. Le damos un nombre (suele ser buena idea darle el mismo nombre que el proyecto), seleccionamos multibranch pipeline y le damos a OK.
3. Le damos a Add source:
   1. Seleccionamos git.
   2. En el repositorio seleccionamos nuestro proyecto de github.
   3. Como el proyecto es público, no nos hace falta introducir el token. Si no, deberíamos añadir usuario y el token como contraseña.
   4. Añadimos dos Behaviours para estar más seguros de que no ocurren errores inesperados en el futuro:
      * Clean after checkout.
      * Clean before checkout.
   5. Por último, seleccionamos la opción "Scan Multibranch Pipeline Triggers". Para el ejercicio, es mejor añadir un tiempo corto, como un minuto. En un ejemplo real este número puede ser más alto.
   6. Guardamos.

En los logs podemos ver que se ha escaneado la rama 'main' y que no se ha encontrado ningún `Jenkinsfile`. El siguiente paso será añadirlo.

## Añadimos el `Jenkinsfile` que ejecuta los tests:
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

## Modificamos el `Jenkinsfile` para que despliegue la aplicación cuando se commitee algo en main:
1. Creamos una nueva rama de desarrollo en la que modificaremos el fichero. Para ello, ejecutamos `git checkout -b dev`.
2. Añadimos en jenkins el plugin "SSH Pipeline Steps". Para ello:
   1. Accedemos a la sección "Administrar Jenkins".
   2. Accedemos a "Administrar Plugins".
   3. Buscamos el plugin "SSH Pipeline Steps" y lo instalamos. Cuidado de no reiniciar pues perderemos la configuración actual.
3. Añadimos un nuevo stage que solo se ejecutará en la rama main y que se conectará por ssh al servidor de producción para hacer el despliegue.
```shell
    stage('Deploy') {
      when {
        branch 'main'
      }
      steps {
        sh 'python3 test.py'
      }
    }
```
4. Añadimos ciertos cambios a la calculadora. Por ejemplo, la multiplicación.
5. Commiteamos y pusheamos los cambios. Vemos que solo se ejecutan los tests.
6. Mergeamos los cambios en main:
   1. Ejecutamos `git checkout main`
   2. Ejecutamos `git merge dev`
   3. Ejecutamos `git push origin main`



