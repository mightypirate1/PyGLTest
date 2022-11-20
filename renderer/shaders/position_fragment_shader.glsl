 #version 330

in float size;
in vec2 v_centroid;
in vec2 v_pos;
in float walltime;

out vec4 f_color;

vec3 color() {
    float r = 0.5 * (1 + sin(walltime));
    float g = 0.5 * (1 + sin(1.1234 * walltime));
    float b = 0.5 * (1 + sin(1.23116324 * walltime));
    return 3.0 * normalize(vec3(r, g, b));
}

float alpha() {
    float d = length(v_pos - v_centroid) / size;
    float sigma0_sq = 0.15 + 0.07 * sin(walltime);
    float sigma1_sq = 0.10 + 0.05 * sin(walltime);
    float gauss0 = exp(-d * d / sigma0_sq);
    float gauss1 = exp(-d * d / sigma1_sq);
    return 3.0 * (gauss0 - gauss1);
}

void main() {
    f_color = vec4(color(), alpha());
}