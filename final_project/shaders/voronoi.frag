#version 330 core

// Passing the UVs to the fragment shader from the vertex one...
in vec2 uv;

// Arguments
uniform vec2 VoronoiPoints[1000];
uniform int NumPoints;
uniform float Opacity; // (0,1]
uniform float PointRadius;
// Output
out vec4 f_color;

vec3 random_color(vec2 seed){
    // Generates a pseudorandom color using a seed.
    // When the frequency is low enough, the regions will have similar colors (try with 0.3)
   float frequency = 2.0;
   return vec3(0.5 + 0.5*sin(frequency*seed), cos(frequency*(seed.x+seed.y)));
}


void main()
{
    float min_distance = distance(uv, VoronoiPoints[0]);
    float point_distance;
    vec2 closest_point = VoronoiPoints[0];
    
    for (int i = 1; i<NumPoints; i++){
        point_distance = distance(uv, VoronoiPoints[i]);
        if (point_distance < min_distance){
            min_distance = point_distance;
            closest_point = VoronoiPoints[i];
        }
    
    }

    vec3 col = random_color(closest_point)
        // Generates a pseudorandom color depending on the closest point's position.
        // This ensures that all of the pixels in the same region have the same color.
        + 2.0 * step(min_distance, PointRadius); 
        // Colors the pixel white if it is close enough to a point.
    // Output to screen
    f_color = vec4(col, Opacity);
}