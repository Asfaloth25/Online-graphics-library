#version 330 core

// Passing the UVs to the fragment shader from the vertex one...
in vec2 uv;

// Arguments
uniform float GridSize; // default 1.0
uniform float LineWidth; // default 0.01;
uniform float Opacity; // (0,1]
uniform vec3 LineColor;
uniform vec3 AxesLineColor;

// Output
out vec4 f_color;



void main()
{
    vec2 distances = mod(uv+GridSize + 0.5*LineWidth, vec2(GridSize));
    float min_distance = min(distances.x, distances.y);
    float is_line = step(min_distance, LineWidth);
    float is_axis = step(min(abs(uv.x), abs(uv.y)), GridSize/8.0);
    vec3 col = is_axis*AxesLineColor + (1.0-is_axis)* LineColor;
    
    f_color = vec4(col, Opacity*is_line);
}