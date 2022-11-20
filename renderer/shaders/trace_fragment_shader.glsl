 #version 330

in vec4 color_p0;
in vec4 color_p1;
in vec2 v_ref_p0;
in vec2 v_ref_p1;
in vec2 v_pos;
in float width;

out vec4 f_color;

float rounding(vec2 p0, vec2 p1, vec2 x, float width) {
    vec2 d = p1 - p0;
    vec2 n = normalize(d.yx * vec2(1, -1));
    float W = width;
    float pad = 1.5;
    float base_rounding = (pad - abs(dot(n, x - p1)) / W);

    if (dot(x - p0, d) < 0.0) {
        // we are "before" the line
        float edge_rounding = pad - length(x - p0) / W;
        return edge_rounding;
    }
    if (dot(x - p1, -d) < 0.0) {
        // we are "before" the line
        float edge_rounding = pad - length(x - p1) / W;
        return edge_rounding;
    }
    return base_rounding;
}

vec4 color(vec2 p0, vec2 p1, vec2 x) {
    vec2 d = p1 - p0;
    float blend = dot(d / length(d), x - p0 / length(d));
    return 1.5 * normalize(blend * color_p1 + (1 - blend) * color_p0);
}

void main() {
    float R = rounding(v_ref_p0, v_ref_p1, v_pos, width);
    vec4 C = color(v_ref_p0, v_ref_p1, v_pos);
    f_color = vec4(1, 1, 1, R) * vec4(C.xyz, 1);
}