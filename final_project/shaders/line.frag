#version 330 core

// Passing the UVs to the fragment shader from the vertex one...
in vec2 uv;

// Arguments
uniform vec2 PointA;
uniform vec2 PointB;
uniform float Opacity; // (0,1]
uniform float LineWidth;
uniform vec3 LineColor;
uniform float IsSegment;

// Output
out vec4 f_color;

float PointScore(vec2 point, vec2 direction){
    vec2 scores = point*direction;
    return scores.x+scores.y;
}

vec2 MeanPoint(vec2 A, vec2 B ){
    return 0.5*(A + B);
}

void main()
{
    vec2 line_direction = normalize(PointB-PointA);
    vec2 orth_line_direction = vec2(line_direction.y, -line_direction.x);
    float uv_score = PointScore(uv, orth_line_direction);
    float distance_to_line = abs(uv_score - PointScore(PointA, orth_line_direction));
    float IsLine = step(distance_to_line, LineWidth);

    vec2 mean_point = MeanPoint(PointA, PointB);
    float seg = IsSegment * step(length(PointB-mean_point), abs(PointScore(uv-mean_point, line_direction)));
    f_color = (1.0-seg) * IsLine * vec4(LineColor, Opacity);
}