from flask import Flask, send_file, request, render_template_string, jsonify
import io
from PIL import Image
from safepython import run_restricted
from code_examples import fetch_examples

app = Flask(__name__)


last_user_code = ''
def render_image(code):
    global last_user_code
    # Run the provided code safely
    # try:

    image = run_restricted(code)
    
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io
    
    # except Exception as e:
    #     print("Error in user code execution:", e)

@app.route('/')
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Librería de Geometría Computacional)</title>
    <!-- CodeMirror CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/codemirror.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/theme/monokai.min.css"> <!-- monokai Theme -->
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }

        #editor {
            border: 1px solid #ccc;
            font-size: 14px;
            height: 300px;
        }

        #output-container {
            margin-top: 20px;
        }

        #output-image {
            width: 100%;
            max-width: 1024px;
            height: 512px;
            background: #ffffff;
            border: 1px solid #ccc;
        }
    </style>
</head>
<body>
    <h1>Librería de Geometría Computacional</h1>
    <h3>Una aplicación web basada en ModernGL y Flask</h3>
    <p>Para ver ejemplos de uso interactivos, <a href="/tutorial">mira aquí la documentación</a></p>


    
    <div id="editor"></div>

    <div id="output-container">
        <img id="output-image" src="" alt="Generated Image"/>
    </div>

    <!-- CodeMirror Scripts -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/codemirror.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/mode/python/python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/addon/edit/closebrackets.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/addon/edit/matchbrackets.min.js"></script>

    <script>
        // Initialize CodeMirror editor
        const editor = CodeMirror(document.getElementById('editor'), {
            mode: 'python',
            theme: 'monokai', // Set the theme here
            lineNumbers: true,
            indentUnit: 4,
            matchBrackets: true,
            autoCloseBrackets: true
        });
                                  

        // Function to update the image
        function updateImage() {
            const code = editor.getValue().trim();

            fetch(`/render`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code: code })
            })
            .then(response => {
                if (response.ok) return response.blob();
                throw new Error('Error generating image');
            })
            .then(blob => {
                const url = URL.createObjectURL(blob);
                document.getElementById('output-image').src = url;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('output-image').src = '';
            });
        }

        // Update image whenever the editor content changes
        editor.on('change', updateImage);
    </script>
                                  
    <h3>Discusión</h3>
    <p>
        Para renderizar las imágenes, esta aplicación utiliza una librería propia basada en ModernGL. 
        ModernGL es una librería de Python que permite interactuar con <a href="https://opengl.org/" target="_blank" style="text-decoration: none; color: #007BFF;">OpenGL</a>, para ejecutar programas
        en la GPU (también conocidos como shaders, y escritos en el lenguaje GLSL). Esto es vital a la hora de realizar cualquier renderizado gráfico, puesto que la GPU, aunque tiene sus limitaciones, es capaz de realizar miles de cálculos en paralelo.
    </p><p>    
        De forma simplificada: cada shader recibe como entrada, entre otras cosas, cada píxel de la imagen y la posición de éste (coordenadas UV). A partir de estos argumentos, debe devolver el color de dicho píxel.
        Esta librería consta de múltiples shaders propios: para colorear el fondo, dibujar la cuadrícula, dibujar puntos y rectas, representar polígonos, dibujar diagramas de Voronoi... 
        Por ejemplo, para dibujar un polígono, un shader comprueba para cada píxel de la pantalla si éste se encuentra dentro del polígono (contando las intersecciones de un segmento a un punto exterior con los lados del polígono).
        Otras funciones, como Quickhull, se ejecutan primero en Python y después se llama a otros shaders para renderizar el resultado.
        
    </p><p>
        Para más información, recomiendo visitar la documentación de las librerías mostradas abajo.
    </p>
</body>
<footer style="background-color: #f1f1f1; padding: 20px; text-align: center; margin-top: 20px;">
    <p>Desarrollado por Marcos Garrido Ferrer</p>
    <p>Bibliografía de recursos utilizados:</p>
    <ul style="list-style: none; padding: 0;">
        <li><a href="https://moderngl.readthedocs.io/" target="_blank" style="text-decoration: none; color: #007BFF;">ModernGL</a></li>
        <li><a href="https://pillow.readthedocs.io/" target="_blank" style="text-decoration: none; color: #007BFF;">Pillow</a></li>
        <li><a href="https://flask.palletsprojects.com/" target="_blank" style="text-decoration: none; color: #007BFF;">Flask</a></li>
        <li><a href="https://restrictedpython.readthedocs.io/" target="_blank" style="text-decoration: none; color: #007BFF;">RestrictedPython</a></li>
        <li><a href="https://codemirror.net/" target="_blank" style="text-decoration: none; color: #007BFF;">CodeMirror</a></li>
    </ul>
</footer>
</html>

    """)

@app.route('/tutorial')
def tutorial_test():
    html = fetch_examples()
    print(html)
    return render_template_string(html)

@app.route('/render', methods=['POST'])
def render():
    data = request.json
    code = data.get('code', '')

    img_io = None

    img_io = render_image(code)

    if img_io:
        # For debugging only: saving the image to file
        debug_image = Image.open(img_io)
        debug_image.save('output.png', format='PNG')
        img_io.seek(0)  # Reset the stream position for the next read
        return send_file(img_io, mimetype='image/png')
    else:
        return jsonify({"error": "Invalid code"}), 400
    




if __name__ == '__main__':
    app.run(debug=True)
