 #version 410

#define MAX_ITER 300
in vec2 v_pos;
in float walltime;

out vec4 f_color;


vec2 complex_mult(vec2 a, vec2 b) {
    return vec2(
        a.x * b.x - a.y * b.y,
        a.x * b.y + a.y * b.x
    );
}

vec2 mandelbrot_iter(vec2 current, vec2 initial) {
    return complex_mult(current, current) + initial;
}

vec4 color(int n) {
    float x = n / float(MAX_ITER);
    vec3 rgb = vec3(1.2, 0.7, 0.4) * x;
    return vec4(rgb, 1);
}

void main() { 
    vec2 current = v_pos;
    vec2 initial = v_pos;
    int n;

    for (n = 0; (n < MAX_ITER && length(current) < 1000); n++) {
        current = mandelbrot_iter(current, initial);
    }

    f_color = color(n);
}