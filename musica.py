import streamlit as st
import moviepy.editor as mp
from pathlib import Path
from pytube import YouTube

# Función para descargar el video
def download_video(url, format):
    try:
        # Descargar el video de YouTube
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video_filename = video.default_filename
        video.download()

        # Obtener la ruta de la carpeta "Descargas"
        download_folder = Path.home() / "Descargas"

        # Mover el archivo descargado a la carpeta "Descargas"
        video_path = Path(video_filename)
        target_path = download_folder / video_path.name
        video_path.rename(target_path)

        # Convertir el video a MP3 si se selecciona el formato "MP3"
        if format == 'MP3':
            mp4_file = str(target_path).replace('.mp4', '.mp3')
            clip = mp.AudioFileClip(str(target_path))
            clip.write_audiofile(mp4_file)
            clip.close()
            target_path.unlink()  # Eliminar el archivo MP4 original después de la conversión a MP3

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
