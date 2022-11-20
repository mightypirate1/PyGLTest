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

void main() {

    gl_Position = vec4(in_vert, 1.0, 1.0);
    size = in_size;
    v_centroid = in_centroid;
    v_pos = in_vert;
    walltime = in_walltime;
}
