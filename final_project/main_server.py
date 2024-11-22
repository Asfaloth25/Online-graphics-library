from flask import Flask, send_file, request, render_template_string, jsonify
import io
from PIL import Image
from safepython import run_restricted
from threading import Thread

app = Flask(__name__)


last_user_code = ''
def render_image(code):
    global last_user_code
    # Run the provided code safely
    try:

        print('GOT HERE 1')
        image = run_restricted(code)
        
        img_io = io.BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        last_user_code = code
        return img_io
    
    except Exception as e:
        print("Error in user code execution:", e)
        return
        return run_restricted(last_user_code, TEST_MODE=True)

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
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/theme/xq-light.min.css"> <!-- xq-light Theme -->
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
            theme: 'xq-light', // Set the theme here
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
</body>
</html>

    """)

@app.route('/render', methods=['POST'])
def render():
    data = request.json
    code = data.get('code', '')

    try:

        def thread_func(code:str, l:list):
            l.append(render_image(code))

        l = []
        t = Thread(target=thread_func, args=(code,l))
        t.start()
        t.join()
        img_io = l[0]
    except Exception as e:
        print('ERROR:', e)
        return

    if img_io:
        # For debugging only: save the image to file
        debug_image = Image.open(img_io)
        debug_image.save('output.png', format='PNG')
        img_io.seek(0)  # Reset the stream position for the next read
        return send_file(img_io, mimetype='image/png')
    else:
        return jsonify({"error": "Invalid code"}), 400
if __name__ == '__main__':
    app.run(debug=True)