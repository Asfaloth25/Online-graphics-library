import moderngl # Shader image rendering
from PIL import Image # Converting the render target (buffer) into an image
import numpy as np 
import array # Quad buffer initialization
import io # Formatting the images so that they can be sent to the webpage
import os # Loading shaders from their folder

class Shader:
    def __init__(self, context:moderngl.Context, aspect_ratio:tuple, render_obj_data, vert_shader:str, frag_shader:str, **kwargs):
        self._CTX = context
        self._ASPECT_RATIO = aspect_ratio
        self._RENDER_OBJ_DATA = render_obj_data
        self._vert_shader = vert_shader
        self._frag_shader = frag_shader
        self._setup_shader(**kwargs)
        self._base_settings = kwargs

    @staticmethod
    def from_file(shader_base_path, vert_shader_name, frag_shader_name, **kwargs):

        contents = []
        for shader_type in (vert_shader_name, frag_shader_name):
            with open(shader_base_path+'/'+shader_type, 'r') as file:
                contents.append(file.read())
        return Shader(*contents, **kwargs)


    def get_setting(self,keyname:str):
        return self._base_settings[keyname]
        
    def _set_shader_values_from_dict(self, values_dict:dict)->None:
        for arg in values_dict:
            self._program[arg] = values_dict[arg]

    def _setup_shader(self, **kwargs)->None:
        '''
        kwargs should include all of the values to set.
        For example:
            self._set_shader(
                palette = np.array(...),
                size = 36.9,
                ...
            )
        '''
        
        
        # 1- Fetching the shader from "moderngl_objects.py" (not applicable in this project)

        # 2- Shader program initialization
        self._program = self._CTX.program(vertex_shader = self._vert_shader, fragment_shader = self._frag_shader)
        self._program['AspectRatio'] = self._ASPECT_RATIO

        # 3- Shader settings
        self._set_shader_values_from_dict(kwargs)

        # 4- Render object
        self._render_obj = self._CTX.vertex_array(self._program, self._RENDER_OBJ_DATA)
        # self.render_obj = GL_OBJ.CTX.vertex_array(self.program, [(GL_OBJ.QUAD_BUFFER, '2f 2f', 'vert', 'texcoord')])

    
    def render(self,**kwargs)->None:
        self._render_shader(**kwargs)

    def _render_shader(self, **kwargs):
        self._set_shader_values_from_dict(kwargs)
        self._render_obj.render(mode=moderngl.TRIANGLE_STRIP)

class ShaderScheduler:

    def __init__(self, image_size:tuple=(1024,512), bgcolor:tuple=(1,1,1)) -> None:

        self._image_size = image_size
        self._CTX = moderngl.create_context(standalone=True)

        # This enables blending between different render passes. I want the shader programs to be executed on top of another,
        # so this makes it possible to pass an "opacity" parameter to programs' fragment shaders such as "voronoi.frag".
        self._CTX.enable(moderngl.BLEND) 


        self._ASPECT_RATIO = self._image_size[0]/self._image_size[1]

        QUAD_BUFFER = self._CTX.buffer(data=array.array('f', [ ## <---- ModernGL VBO (see documentation)
        ### Position (x,y), UV coords (x,y)
        # OpenGL thinks of coordinates differently than pygame (the latter inverts the y axis)
        # These can be written all in the same line but they will be interpreted the same way, and it is more visual this way.
            -1.0, 1.0, 0.0, 0.0, # Topleft
            1.0, 1.0, 1.0, 0.0, # Topright
            -1.0, -1.0, 0.0, 1.0, # Bottomleft
            1.0, -1.0, 1.0, 1.0 # Bottomright
        ]))

        self._RENDER_OBJ_DATA = [(QUAD_BUFFER, '2f 2f', 'vert', 'texcoord')] # <---- Will feed this to the VAO


        self._PRIORITY_STACK = []
        self._STACK = []

        self._OUTPUT_BUFFER = self._CTX.simple_framebuffer(image_size)
        self.bgcolor = bgcolor
        self.OPTIONS = {
            'CentrePos': (0,0),
            'AspectRatio': 2,
            'Zoom': 1
        }
        self.SHADERS = self._load_shaders('./shaders')

    def load_functions(self):
        return load_functions_to_scheduler(self)

    def stack(self, priority:bool=False):
        def decorator(func):
            def wrapper(*args, **kwargs):
                (self._STACK, self._PRIORITY_STACK)[priority].append((func, args, kwargs))
            return wrapper
        return decorator
    
    def _load_shaders(self, shader_base_path:str) -> dict[str, Shader]:
        SHADERS = {}
        with open(f'{shader_base_path}/uv_geometry.vert', 'r') as file:
            vertex_shader = file.read()
        for filename in os.listdir(shader_base_path):
            name, extension = filename.split('.')
            if extension == 'frag':
                with open(f'{shader_base_path}/{filename}', 'r') as file:
                    fragment_shader = file.read()
                SHADERS[name] = Shader(self._CTX, self._ASPECT_RATIO, self._RENDER_OBJ_DATA, vertex_shader, fragment_shader)

        return SHADERS
    
    def set_shader_parameters(self, **kwargs):
        for shader in self.SHADERS:
            self.SHADERS[shader]._set_shader_values_from_dict(kwargs)

    def draw_background(self, color:tuple):
        self._OUTPUT_BUFFER.clear(*color, 1)
        
    def _execute_stack(self):
        for stack in (self._PRIORITY_STACK, self._STACK):
            for command in stack:
                command[0](*command[1], **command[2])
            stack.clear()

    def render_image(self, TEST_MODE:bool=False) -> io.BytesIO:
        self._OUTPUT_BUFFER.use()
        self.draw_background(self.bgcolor)

        self.set_shader_parameters(**self.OPTIONS)

        self._execute_stack()

        data = self._OUTPUT_BUFFER.read(components=4)
        image = Image.frombytes('RGBA', self._image_size, data).transpose(Image.FLIP_TOP_BOTTOM)
        

        # for debugging purposes
        if TEST_MODE:
            image.show()

        return image




def load_functions_to_scheduler(scheduler:ShaderScheduler)->dict:
    @scheduler.stack(priority=True)
    def BackgroundColor(color:tuple=(255,255,255)):
        scheduler.draw_background(np.array(color) / 255)

    @scheduler.stack(priority=True)
    def CenterCamera(center_pos:tuple=(0,0)):
        scheduler.set_shader_parameters(CentrePos = center_pos)
        #scheduler.OPTIONS['CentrePos'] = center_pos

    @scheduler.stack(priority=True)
    def SetZoom(zoom:float = 1):
        scheduler.set_shader_parameters(Zoom = zoom)
        #scheduler.OPTIONS['Zoom'] = zoom

    @scheduler.stack()
    def Grid(gridsize:float=1, linewidth:float=0.01, opacity:float=1, linecolor:tuple=(0,0,0), axeslinecolor:tuple=(255,0,0)):
        scheduler.SHADERS['grid'].render(
            GridSize = gridsize,
            LineWidth = linewidth,
            Opacity = opacity, 
            LineColor = linecolor,
            AxesLineColor = axeslinecolor
        )
        
    @scheduler.stack()
    def Voronoi(points:list[tuple], opacity:float=0.5, pointradius:float=0.025):
        MAXVORONOIPOINTS = 1000
        numpoints = len(points)
        points_converted = np.array(points)
        if numpoints < MAXVORONOIPOINTS:
            padding = np.zeros((MAXVORONOIPOINTS-numpoints, 2), dtype='f4')
            points_converted = np.vstack([points_converted, padding])
        scheduler.SHADERS['voronoi'].render(
            VoronoiPoints = points_converted,
            Opacity = opacity,
            PointRadius = pointradius,
            NumPoints = numpoints
        )

    @scheduler.stack()
    def Points(points:list[tuple], opacity:float=0.5, pointradius:float=0.025, pointcolor:tuple=(0,0,0)):
        MAXPOINTS = 1000
        numpoints = len(points)
        points_converted = np.array(points)
        if numpoints < MAXPOINTS:
            padding = np.zeros((MAXPOINTS-numpoints, 2), dtype='f4')
            points_converted = np.vstack([points_converted, padding])
        scheduler.SHADERS['points'].render(
            Points = points_converted,
            Opacity = opacity,
            PointRadius = pointradius,
            NumPoints = numpoints,
            PointColor = pointcolor
        )

    @scheduler.stack()
    def Line(points, opacity:float=0.9, linewidth:float=0.025, linecolor:tuple=(0,0,0)):

        scheduler.SHADERS['line'].render(
            PointA = points[0],
            PointB = points[1],
            LineColor = linecolor,
            LineWidth = linewidth,
            Opacity = opacity,
            IsSegment = 0
        )



    @scheduler.stack()
    def Segment(points, opacity:float=0.9, linewidth:float=0.025, linecolor:tuple=(0,0,0)):
        
        scheduler.SHADERS['line'].render(
            PointA = points[0],
            PointB = points[1],
            LineColor = linecolor,
            LineWidth = linewidth,
            Opacity = opacity,
            IsSegment = 1
        )


    @scheduler.stack()
    def Polygon(points, opacity:float=0.9, linewidth:float=0.025, linecolor:tuple=(0,0,0)):
        for i, vert in enumerate(points):
            Segment(
                (points[i-1], vert),
                opacity=opacity,
                linewidth=linewidth,
                linecolor=linecolor
            )

    return {
        'Voronoi': Voronoi,
        'Grid': Grid,
        'SetZoom': SetZoom,
        'CenterCamera': CenterCamera,
        'BackgroundColor': BackgroundColor,
        'Line': Line,
        'Segment': Segment,
        'Polygon': Polygon,
        'Points': Points
    }



if __name__ == '__main__':
    
    scheduler = ShaderScheduler(image_size=(1024, 512), bgcolor=(1,1,1))
    functions = scheduler.load_functions()
    functions['SetZoom'](1)
    functions['CenterCamera']((0, 0))
    functions['BackgroundColor']((230,230,255))
    functions['Grid'](gridsize=0.25, linewidth=0.005, opacity=0.2)
    functions['Grid'](gridsize=1)
    functions['Voronoi'](2*np.random.rand(20,2) - 1, opacity=0.4)
    scheduler.render_image(TEST_MODE=True)