#importacion del modulo para trabajar con el framework
from flask import Flask, render_template,request
from pytube import YouTube
import re
import os
def validaUrl(urlU):
    patron_youtube_especifico = re.compile(r"https://youtu\.be/[a-zA-Z0-9_-]+\?si=[a-zA-Z0-9_-]+")
    coincidencia = patron_youtube_especifico.match(urlU)
    return bool(coincidencia)

def descargarAudio(urlU):
    if validaUrl(urlU):
        try:
            video=YouTube(urlU)#objeto para encontrar el video de la url
            print("Descargando "+video.title+" ...")
            audio=video.streams.filter(only_audio=True).first()

            # Obtiene la ruta de la carpeta de descargas del usuario
            carpeta_descargas = os.path.join(os.path.expanduser('~'), 'Downloads')
            out_file = audio.download(output_path=carpeta_descargas) 
            # guarda el archivo y convierte a mp3
            base, ext = os.path.splitext(out_file) 
            nuevo_archivo = base + '.mp3'
            os.rename(out_file, nuevo_archivo) 
            # muestra el resultado del proceso
            print(video.title + " Descargado correctamente :)")
        except:
            print("Error en la descarga, puede ser que este archivo ya exista en la ruta de descargas")
    else:
        print("URL no valida")

def descargaVideo(urlUser):
    if validaUrl(urlUser):
        try:
            yt=YouTube(urlUser)#objeto para encontrar el video de la url
            print("Descargando "+yt.title+" ...")
            video=yt.streams.get_highest_resolution()#obtiene la mas alta calidad del video
            # Obtiene la ruta de la carpeta de descargas del usuario
            carpeta_descargas = os.path.join(os.path.expanduser('~'), 'Downloads')
            #Guarda el video en la carpeta de descargas
            out_file=video.download(output_path=carpeta_descargas)
            print(video.title + " Descargado correctamente")
        except:
            print("Error en la descarga, puede ser que este archivo ya exista en la ruta de descargas")
    else:
        print("URL no valida")


app=Flask(__name__)#creacion de la aplicacion
#CREACION DE RUTAS:
@app.route('/', methods=['GET','POST'])#definicion de la ruta raiz 
def principal():#pagina principal
    """Manera de recibir datos con el metodo GET
    if request.args:
        urlUser= request.args['url']#Recibe el dato de la url
        if validaUrl(urlUser):
            descargarAudio(urlUser)
            request.args.clear
        else:
            print("URL no valida")
            request.args.clear
            """
    if request.method == 'POST': #Manera de recibir datos con el metodo POST
        urlUser= request.form['url']#Recibe el dato de la url
        format = request.form['formato']#Recibe el formato de descagar mp3 o mp4
        #Condiciones para descargar
        if format == 'Descargar mp3':
            descargarAudio(urlUser)
        elif format == 'Descargar mp4':
            descargaVideo(urlUser)
    #regresa la pagina principal en html
    return render_template('/index.html')

@app.route('/usuario')#cambia de pagina 
def usuario():
    return "pagina del usuario"


if __name__ == '__main__':#creacion del servidor
    #debug =True indica que se está en proceso de desarrollo y actualiza el servidor
    app.run(debug=True)
