#version 330 core

// Passing the UVs to the fragment shader from the vertex one...
in vec2 uv;

// Arguments
uniform vec2 Vertices[1000];
uniform int NumVertices;
uniform float Opacity; // (0,1]
uniform vec3 InfillColor;

// Output
out vec4 f_color;


float signed_area(vec2 A, vec2 B, vec2 C){
    mat3 M = mat3(
        1.0, 1.0, 1.0,
        A.x, B.x, C.x,
        A.y, B.y, C.y
    );
    return determinant(M);
}

void main(){

    bool below;
    bool last_below = (Vertices[0].y < uv.y);
    float intersection_count = 0.0;
    
    for (int i = 1; i < NumVertices; i++)
    {
        below = (Vertices[i].y < uv.y);
        if (below != last_below){
            if (below){
                if (signed_area(Vertices[i], uv, Vertices[i-1])<0)
                {
                    intersection_count++;
                }
            }
            else if (signed_area(Vertices[i], uv, Vertices[i-1])>0){
                intersection_count++;
            }
        }
        last_below = below;
    }

    // The last segment (from the last point to the first one)
    below = (Vertices[0].y < uv.y); 
    if (below != last_below){
        if (below){
            if (signed_area(Vertices[0], uv, Vertices[NumVertices-1])<0)
            {
                intersection_count++;
            }
        }
        else if (signed_area(Vertices[0], uv, Vertices[NumVertices-1])>0){
            intersection_count++;
        }
    }

    float is_inside = mod(intersection_count, 2.0);
    f_color = vec4(InfillColor, Opacity * is_inside);
}