"""
    Following example of ripple-mesh reformer from the book->
    Muhammad Mobeen Movania - OpenGL development cookbook-Packt Publishing (2013) 
"""

import moderngl_window as mglw
import numpy as np
from pyrr import Matrix44

class RippleMesh(mglw.WindowConfig):
    gl_Version = (3,3)
    window_size = (800, 600)
    title = "Ripple Mesh"
    resizable = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.prog = self.ctx.program(
            vertex_shader='''
            #version 330 core
            
            layout(location=0) in vec2 vVertex;
            uniform mat4 MVP;
            uniform float time;
            
            const float amplitude = 0.125;
            const float frequency = 4;
            const float PI = 3.14159;
            
            out vec3 f_color;
            void main()
            {
                //float distance = length(vVertex - 0.75);
                float distance = length(vVertex);
                
                float z = amplitude*sin(PI*distance*frequency+time);
                gl_Position = MVP*vec4(vVertex.x, vVertex.y, z, 1);
            }
            ''',
            fragment_shader='''
            #version 330 core
            layout(location=0) out vec4 vFragColor;
            
            void main()
            {
                vFragColor = vec4(1,1,1,1);
            }
            '''
        )
        # grid of size-NxM on the x-z plane
        N, M = 33,33
        # size in unit of coordinates
        SIZE_X, SIZE_Z = 1.5, 1.5
        vertices = []
        for i in range(M + 1):
            for j in range(N + 1):
                x = (SIZE_X/N)*j - (SIZE_X/2)
                y = (SIZE_Z/M)*i - (SIZE_Z/2)
                vertices.extend([x,y])
        indices = []
        for i in range(M):
            for j in range(N):
                i0 = (i*(N+1)+j)
                i1 = i0 + 1
                i2 = (N+1) + i0
                i3 = (N+1) + i0 + 1
                if (j + i)%2 == 0:
                    indices.extend([i0,i1,i2, i1,i3,i2])
                else:
                    indices.extend([i0,i2,i3, i0,i3,i1])

        vertices = np.array(vertices).astype('f4')
        indices = np.array(indices).astype(np.uint32)


        self.vbo = self.ctx.buffer(vertices)
        self.ibo = self.ctx.buffer(indices)
        content = [(self.vbo, '2f', 'vVertex')]
        self.vao = self.ctx.vertex_array(self.prog, content, index_buffer=self.ibo)        
    def render(self, time: float, frame_time: float):
        self.ctx.clear(0,0,0, 1.0)
        self.ctx.enable(self.ctx.DEPTH_TEST)
        self.ctx.wireframe = True

        proj = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 1000.0)
        lookat = Matrix44.look_at(
            (1.5, 1.5, 1.5),
            (0.0, 0.0, 0.1),
            (0.0, 0.0, 1.0),
        )

        self.prog['MVP'].write((proj*lookat).astype('f4'))
        self.prog['time'] = time
 
        self.vao.render(mode=self.ctx.TRIANGLES)

if __name__ == '__main__':
    RippleMesh.run()

