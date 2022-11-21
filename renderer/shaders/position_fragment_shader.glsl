 #version 330

in float size;
in vec2 v_centroid;
in vec2 v_pos;
in float walltime;

out vec4 f_color;

vec3 color() {
    float r = 0.5 * (1.3 + 0.3 * sin(walltime));
    float g = 0.5 * (1.3 + 0.3 * sin(1.1234 * walltime));
    float b = 0.5 * (1.3 + 0.3 * sin(1.23116324 * walltime));
    return 5.0 * normalize(vec3(r, g, b));
}

float alpha() {
    float d = length(v_pos - v_centroid) / size;
    float sigma0 = 0.25 + 0.1 * sin(walltime);
    float sigma1 = 0.15 + 0.15 * sin(walltime);
    float gauss0 = exp(-d * d / pow(sigma0, 3));
    float gauss1 = exp(-d * d / pow(sigma1, 3));
    return 7.0 * (gauss0 - gauss1);
}

void main() {
    // f_color = vec4(20 * v_dist_to_centroid);
    f_color = vec4(1, 1, 1, alpha());
    // f_color = vec4(color(), alpha());
}