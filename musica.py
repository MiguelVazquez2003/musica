import streamlit as st
from pytube import YouTube
import os
import shutil
from pydub import AudioSegment

# Función para descargar el video
def download_video(url, format):
    try:
        # Descargar el video de YouTube
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video_filename = video.default_filename
        video.download()

        # Obtener la ruta de la carpeta "Descargas"
        download_folder = os.path.expanduser("~/Descargas")

        # Mover el archivo descargado a la carpeta "Descargas"
        video_path = os.path.join(os.getcwd(), video_filename)
        target_path = os.path.join(download_folder, video_filename)
        shutil.move(video_path, target_path)

        # Convertir el video a MP3 si se selecciona el formato "MP3"
        if format == 'MP3':
            mp3_filename = video_filename.replace('.mp4', '.mp3')
            mp3_path = os.path.join(download_folder, mp3_filename)
            audio = AudioSegment.from_file(target_path)
            audio.export(mp3_path, format='mp3')
            os.remove(target_path)

        st.success('Descarga completada.')

    except Exception as e:
        st.error(f'Error: {str(e)}')

# Configuración de la página de Streamlit
st.title('Descargar video de YouTube')
# Añadir descripción
st.markdown("""
Esta aplicación te permite descargar videos de YouTube. Simplemente ingresa el enlace del video y selecciona el formato de descarga. Haz clic en el botón "Descargar" para iniciar el proceso de descarga. Una vez completada la descarga, se mostrará un mensaje de éxito y se reproducirán animaciones para indicar que la descarga ha finalizado. ¡Disfruta descargando tus videos favoritos!
""")

st.write('Ingrese el enlace de YouTube y seleccione el formato de descarga.')

# Entrada de URL de YouTube
url = st.text_input('Ingrese el enlace de YouTube')

# Selección de formato
format = st.selectbox('Seleccione el formato de descarga', ['MP4', 'MP3'])

# Botón de descarga
if st.button('Descargar'):
    if url:
        st.info('Descargando...')
        download_video(url, format)
    else:
        st.warning('Ingrese un enlace de YouTube válido.')

    # Añadir animaciones y barra de progreso
    with st.spinner('Procesando...'):
        st.success('Descarga completada')
        st.balloons()
