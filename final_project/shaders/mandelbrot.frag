#version 330 core

// Passing the UVs to the fragment shader from the vertex one...
in vec2 uv;

// Arguments
uniform int MandelbrotSteps;
uniform float Opacity;
uniform vec3 MandelbrotSetColor;
//Output
out vec4 f_color;




vec2 pow_2_complex(vec2 complex){
    return vec2(pow(complex.x,2.0) - pow(complex.y, 2.0), 2.0*complex.x*complex.y);
}

float IsMandelbrot( vec2 pos, int n_iters ) {
    highp vec2 z_n = pos;
    for (int i = 0; i < n_iters; i++){
        z_n = pow_2_complex(z_n) + pos;
        if (length(z_n) > 2.0) {
            discard;
        }
    }
    return 1.0;
}

void main()
{
    f_color = vec4(MandelbrotSetColor * IsMandelbrot(uv, MandelbrotSteps), Opacity);
}
