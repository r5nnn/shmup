#version 330 core

vec3 vertices[3] = vec3[](
    vec3(0.0, 0.4, 0.0),
    vec3(-0.4, -0.3, 0.0),
    vec3(0.4, -0.3, 0.0)
);

void main() {
    gl_Position = vec4(vertices[gl_VertexID], 1.0);
}