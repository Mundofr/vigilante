from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import re
import shutil

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"

# Crear carpeta si no existe
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def clean_filename(s):
    # Limpiar caracteres no válidos para archivos
    return re.sub(r'[\\/*?:"<>|]', "", s)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/terminos-y-privacidad')
def terminos():
    return render_template('terminosyprivacidad.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format = request.form['format']

    try:
        ydl_opts = {
            'quiet': True,
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),  # Guardar con título original
            'no_warnings': True,
        }

        if format == 'mp3':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'postprocessor_args': ['-ar', '44100'],
                'prefer_ffmpeg': True,
                'keepvideo': False,
            })
            ext = 'mp3'

        elif format == 'mp4':
            ydl_opts.update({
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
            })
            ext = 'mp4'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict.get('title', 'video')
            clean_title = clean_filename(title)
            file_path = os.path.join(DOWNLOAD_FOLDER, f"{clean_title}.{ext}")

        # Enviar archivo para descarga
        response = send_file(file_path, as_attachment=True)

        # Opcional: eliminar archivo después de enviar (para no llenar espacio)
        # IMPORTANTE: Esto funciona solo si no se usa modo debug en Flask y el servidor sirve bien el archivo antes de eliminar
        @response.call_on_close
        def cleanup():
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error eliminando archivo: {e}")

        return response

    except Exception as e:
        return f"<h2>Error: {str(e)}</h2>"

if __name__ == '__main__':
    app.run(debug=True)
