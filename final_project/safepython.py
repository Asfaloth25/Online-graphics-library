from RestrictedPython import compile_restricted
from RestrictedPython import safe_globals
from RestrictedPython.Guards import guarded_iter_unpack_sequence
from RestrictedPython.Eval import default_guarded_getiter, default_guarded_getitem


# Safe functions and modules
import math, numpy
import time
import ShaderScheduler



SAFE_FUNCTIONS = {
    'np': numpy,
    'math': math,
    'time': time,
    '_getiter_': default_guarded_getiter, # These two enable the usage of for loops
    '_iter_unpack_sequence_': guarded_iter_unpack_sequence,
    '_getitem_': default_guarded_getitem
}



def run_restricted(user_code:str, TEST_MODE:bool=False):

    # Compiling the user code into a restricted AST
    byte_code = compile_restricted(user_code, filename="<string>", mode="exec")
    
    # Defining the restricted environment
    scheduler = ShaderScheduler.ShaderScheduler(image_size=(2048,1024))
    shader_functions = scheduler.load_functions()
    safe_env = SAFE_FUNCTIONS | safe_globals | shader_functions # The "|" operation returns a sum of the three dictionaries
    
    # Executing user code
    exec(byte_code, safe_env)
    print("Code executed successfully.")

    print(scheduler._STACK)
    return scheduler.render_image(TEST_MODE=TEST_MODE)



if __name__ == '__main__':
    user_code = '''
SetZoom(1)
CenterCamera((0, 0))
BackgroundColor((230,230,255))
for i in range(2):
    Grid(gridsize=0.5+0.5*i, linewidth=0.005 + 0.005*i, opacity=0.2 + 0.8*i)
Voronoi(2*np.random.rand(20,2) - 1, opacity=0.8)
    '''

    run_restricted(user_code, TEST_MODE=True)
