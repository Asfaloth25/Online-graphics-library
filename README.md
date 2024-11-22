# Online graphics library

## Description:
This is a small graphics library with some computational geometry algorithms (Voronoi, Quickhull, Delaunay triangulation...). 

When executed, a web application will be launched. Said webpage consists of code cells in which the user can write Python code (such as the ones in _Jupyter Notebooks_). The output of the user's code is displayed graphically in the page.

## Details:
This library is written in Python, and uses [*Flask*](https://flask.palletsprojects.com/en/stable/) as a backend for the web application. Flask handles routing, requests and serves as a 
In order to render the images, [*ModernGL*](https://moderngl.readthedocs.io/en/5.8.2/) is employed. Hence, all of the different Python functions the user can call relies on its own OpenGL shader program backend.

## Security:
The Python environment the user interacts with is, naturally, protected. *Restrictedpython* ensures the user's code is harmless before executing it. However, be careful when using this library, as there may still be security issues I am not currently aware of.
For more information on *Restrictedpython*, visit [this page](https://restrictedpython.readthedocs.io/en/latest/idea.html).
