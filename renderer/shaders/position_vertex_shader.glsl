#version 330

in vec2 in_vert;
in float in_size;
in vec2 in_centroid;
in float in_walltime;
in mat4 proj_mtx;

// Goes to the fragment shader
out float size;
out vec2 v_centroid;
out vec2 v_pos;
out float walltime;
out float v_dist_to_centroid;

vec2 proj(vec2 x) {
    return (proj_mtx * vec4(x, 0.0, 1.0)).xy;
}
vec4 proj(vec4 x) {
    return proj_mtx * x;
}

void main() {
    gl_Position = proj(vec4(in_vert,0,1));
    v_centroid = proj(in_centroid);
    v_pos = proj(in_vert);
    size = in_size; // / proj_mtx[0][0];
    walltime = in_walltime;
}
