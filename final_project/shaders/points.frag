#version 330 core

// Passing the UVs to the fragment shader from the vertex one...
in vec2 uv;

// Arguments
uniform vec2 Points[1000];
uniform int NumPoints;
uniform float Opacity; // (0,1]
uniform float PointRadius;
uniform vec3 PointColor;


// Output
out vec4 f_color;

vec4 get_color(){
    for (int i = 0; i<NumPoints; i++){
        if (distance(uv, Points[i]) < PointRadius){
            return vec4(PointColor, Opacity);
            }
    }
    return vec4(0.0);
}

void main()
{
    f_color = get_color();
}