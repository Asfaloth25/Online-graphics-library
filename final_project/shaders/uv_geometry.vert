#version 330 core

in vec2 vert;
in vec2 texcoord;
out vec2 uv;

uniform float AspectRatio;
uniform float Zoom; // 0.0 < Zoom
uniform highp vec2 CentrePos;


void main(){
    uv = texcoord - vec2(0.5); // Making the UVs range from (-0.5, 0.5) in both axes...
    uv = vec2(uv.x * AspectRatio, uv.y); // Scaling the X axis with the Aspect Ratio...
    uv = 2.0*(uv)/Zoom + CentrePos; // One final scaling so that the Y axis ranges from -1 to 1. Centering the camera on "CentrePos".
    gl_Position = vec4(vert.x, -vert.y, 0.0, 1.0);  // The Y axis is inverted... may have to remove this because this is inherent to Pygame.
}