#version 330

in float in_width;
in vec2 in_vert;
in vec2 in_ref_p0;
in vec2 in_ref_p1;
in vec4 in_color_p0;
in vec4 in_color_p1;
in mat4 proj_mtx;

// Goes to the fragment shader
out vec4 color_p0;
out vec4 color_p1;
out vec2 v_ref_p0;
out vec2 v_ref_p1;
out vec2 v_pos;
out float width;

void main() {
    vec4 projected_vert = proj_mtx * vec4(in_vert, 0.0, 1.0);
    gl_Position = projected_vert;
    color_p0 = in_color_p0;
    color_p1 = in_color_p1;
    v_ref_p0 = (proj_mtx * vec4(in_ref_p0, 0, 1)).xy;
    v_ref_p1 = (proj_mtx * vec4(in_ref_p1, 0, 1)).xy;
    width = in_width;
    v_pos = projected_vert.xy;
    
}