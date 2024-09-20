#version 330 core

uniform vec2 iResolution;
uniform float iTime;
uniform sampler2D iChannel0;  // Texture input

#define NUM 9.0

float noise(in vec2 x) {
    vec2 p = floor(x);
    vec2 f = fract(x);
    vec2 uv = p.xy + f.xy * f.xy * (3.0 - 2.0 * f.xy);
    return texture(iChannel0, (uv + 0.5) / 256.0).x;  // Use texture iChannel0
}

float map(in vec2 x, float t) {
    return noise(2.5 * x - sin(6.2831 * t / 15.0 + vec2(1.5, 0.0)));
}

float shapes(in vec2 uv, in float r, in float e) {
    float p = pow(32.0, r - 0.5);
    float l = pow(pow(abs(uv.x), p) + pow(abs(uv.y), p), 1.0 / p);
    float d = l - pow(r, 0.6) - e * 0.2 + 0.05;
    float fw = fwidth(d) * 0.5;
    fw *= 1.0 + 10.0 * e;
    return (r)*smoothstep(fw, -fw, d) * (1.0 - 0.2 * e) * (0.4 + 0.6 * smoothstep(-fw, fw, abs(l - r * 0.8 + 0.05) - 0.1));
}

void main() {
    vec2 fragCoord = gl_FragCoord.xy;
    vec2 qq = fragCoord / iResolution.xy;
    vec2 uv = fragCoord / iResolution.xx;

    uv *= 1.5;
    float time = 11.0 + (iTime + 0.8 * sin(iTime)) / 1.8;
    uv += 0.01 * noise(12.0 * uv + 0.1 * time);

    vec3 col = 0.0 * vec3(1.0) * 0.15 * abs(qq.y - 0.5);

    vec2 pq, st;
    float f;
    vec3 coo;

    // teal
    pq = floor(uv * NUM) / NUM;
    st = fract(uv * NUM) * 2.0 - 1.0;
    coo = (vec3(0.5, 0.7, 0.7) + 0.3 * sin(10.0 * pq.x) * sin(13.0 * pq.y)) * 0.6;
    col += 1.0 * coo * shapes(st, map(pq, time), 0.0);
    col += 0.6 * coo * shapes(st, map(pq, time), 1.0);

    // orange
    pq = floor(uv * NUM + 0.5) / NUM;
    st = fract(uv * NUM + 0.5) * 2.0 - 1.0;
    coo = (vec3(1.0, 0.5, 0.3) + 0.3 * sin(10.0 * pq.y) * cos(11.0 * pq.x)) * 1.0;
    col += 1.0 * coo * shapes(st, 1.0 - map(pq, time), 0.0);
    col += 0.4 * coo * shapes(st, 1.0 - map(pq, time), 1.0);

    col *= pow(16.0 * qq.x * qq.y * (1.0 - qq.x) * (1.0 - qq.y), 0.05);
    gl_FragColor = vec4(col, 1.0);
}