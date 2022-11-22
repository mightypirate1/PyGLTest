#version 410

in vec2 in_vert;
in mat4 proj_matrix;
in float in_walltime;

// Goes to the fragment shader
out vec2 v_pos;
out float walltime;

vec2 proj(vec2 vec) {
    return (proj_matrix * vec4(vec, 1.0, 1.0)).xy;
}

void main() {
    gl_Position = vec4(in_vert, 1, 1);
    v_pos = proj(in_vert);
    walltime = in_walltime;
}
