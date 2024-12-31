import os

js_code_to_fill = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tutorial Page</title>
    <!-- CodeMirror CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/codemirror.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/theme/monokai.min.css">

    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }

        .tutorial-cell {
            margin-bottom: 40px;
        }

        .tutorial-description {
            font-size: 16px;
            margin-bottom: 10px;
            color: #333;
        }

        .editor {
            border: 1px solid #ccc;
            font-size: 14px;
            height: 300px;
        }

        .output-image {
            margin-top: 10px;
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
    <h3>Instrucciones y ejemplos de uso</h3>
    <p>Volver a la <a href="/">página principal</a></p>

    <div class="tutorial-container">
        <!-- Cells will be dynamically added here -->
    </div>

    <!-- CodeMirror Scripts -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/codemirror.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/mode/python/python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/addon/edit/closebrackets.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.12/addon/edit/matchbrackets.min.js"></script>

    <script>
        // Preset tutorial code snippets with explanations
        const tutorialSnippets = [
<REEMPLAZAR>
        ];

        const container = document.querySelector('.tutorial-container');

        // Function to create a tutorial cell
        function createTutorialCell(snippet) {
            // Create wrapper for the tutorial cell
            const cell = document.createElement('div');
            cell.className = 'tutorial-cell';
            cell.dataset.id = snippet.id;

            // Add a paragraph for the description
            const description = document.createElement('p');
            description.className = 'tutorial-description';
            description.textContent = snippet.description;

            // Create CodeMirror editor container
            const editorDiv = document.createElement('div');
            editorDiv.className = 'editor';

            // Create output image container
            const img = document.createElement('img');
            img.className = 'output-image';
            img.alt = 'Generated Output';

            // Append description, editor, and image to the cell
            cell.appendChild(description);
            cell.appendChild(editorDiv);
            cell.appendChild(img);

            // Add the cell to the container
            container.appendChild(cell);

            // Initialize CodeMirror editor
            const editor = CodeMirror(editorDiv, {
                value: snippet.code,
                mode: 'python',
                theme: 'monokai',
                lineNumbers: true,
                indentUnit: 4,
                matchBrackets: true,
                autoCloseBrackets: true,
            });

            // Function to update the image for this cell
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
                    img.src = url;
                })
                .catch(error => {
                    console.error('Error:', error);
                    img.src = ''; // Clear image on error
                });
            }

            // Update image immediately on load
            updateImage();

            // Attach debounced change listener to update the image
            const debouncedUpdateImage = debounce(updateImage, 500);
            editor.on('change', debouncedUpdateImage);
        }

        // Debounce utility function
        function debounce(func, delay) {
            let timeout;
            return function (...args) {
                clearTimeout(timeout);
                timeout = setTimeout(() => func.apply(this, args), delay);
            };
        }

        // Initialize all tutorial cells
        tutorialSnippets.forEach(createTutorialCell);
    </script>
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

'''

BASE_EXAMPLE_PATH = 'code_examples'

def fetch_examples() -> str:
    js_string = ''
    examples = os.listdir(BASE_EXAMPLE_PATH)
    for i, ex in enumerate(examples):
        ex_name = ex.split('.')[0]

        with open(BASE_EXAMPLE_PATH + '/' +ex, 'r', encoding='utf-8') as file:
            file_text = file.read()

        explanation, code = file_text.split('<DELIMITADOR>')
        endline = '\n'
        ex_string = f'''
                code: `{code.strip()}`,
                id: "{ex_name}",
                description: "{explanation.strip().replace(endline, ' ')}"
'''
        js_string += '{' + ex_string + '}' + (','+endline)*(i!=len(examples)-1)

    return js_code_to_fill.replace('<REEMPLAZAR>', js_string)