import numpy as np
import moderngl
import moderngl_window as mglw
from pathlib import Path
from time import time


SHADER_ROOT = Path(__file__).parent / "shaders"
FRACTAL_VERTEX_SHADER = SHADER_ROOT / "fractal_vertex_shader.glsl"
FRACTAL_FRAGMENT_SHADER = SHADER_ROOT / "fractal_fragment_shader.glsl"

class WindowConf(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "ModernGL WindowConf"
    window_size = (1920, 1080)
    aspect_ratio = 16 / 9
    resizable = True


class FractalRenderer(WindowConf):
    title = "Fractal"

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._last_vertex_update_time = 0
        self.ctx.enable(moderngl.BLEND)
        self.init_time = time()
        self.create_matrices()
        self.refresh()
    
    def create_matrices(self):
        self.matrices = {
            "translation": np.eye(4),
            "scale": np.diag([self.aspect_ratio, 1, 1, 1]),
            "rotation": np.eye(4),
        }

    def generate_quad(self):
        return np.array(
            [-1, -1, 1, -1, -1, 1] + [-1, 1, 1, 1, 1, -1],
            dtype="f4",
        )

    def generate_matrix(self):
        return np.matmul(
            self.matrices["scale"],
            self.matrices["translation"],
            dtype="f4",
        )

    def generate_static_content(self):
        T = time() - self.init_time
        contents = [T]
        return np.array(contents, dtype="f4")


    def read_shaders(self):
        def _read_shader_file(path):
            with open(path, "r") as f:
                return f.read()
        shader_path_dict = {
            "fractal_vertex_shader": FRACTAL_VERTEX_SHADER,
            "fractal_fragment_shader": FRACTAL_FRAGMENT_SHADER,
        }
        return {shader: _read_shader_file(shader_path) for shader, shader_path in shader_path_dict.items()}
    

    def refresh(self):
        shader_dict = self.read_shaders()
        self.prog = self.ctx.program(
            vertex_shader=shader_dict["fractal_vertex_shader"],
            fragment_shader=shader_dict["fractal_fragment_shader"],
        )
        self.quad_vbo = self.ctx.buffer(self.generate_quad())
        self.matrix_vbo = self.ctx.buffer(self.generate_matrix())
        self.constant_vbo = self.ctx.buffer(self.generate_static_content())
        print(self.generate_static_content())
        self.vao = self.ctx.vertex_array(
            self.prog,
            [
                (self.quad_vbo, '2f', 'in_vert'),
                (self.matrix_vbo, '16f /r', 'proj_matrix'),
                (self.constant_vbo, '1f /r', 'in_walltime'),
            ],
        )

    def mouse_drag_event(self, x, y, dx, dy):
        mouse_change = 2 * np.array([-dx, dy, 0, 0]) / np.array([*self.window_size, 1, 1])
        matrix = self.generate_matrix()
        new_translation = np.matmul(matrix, mouse_change)
        self.matrices["translation"][3,:2] += np.clip(new_translation[:2], -3, 3)

    def mouse_scroll_event(self, x_offset: float, y_offset: float):
        zoom_factor = 1.05 ** -y_offset
        self.matrices["scale"] *= np.diag([zoom_factor, zoom_factor, 1, 1])
    
    def key_event(self, key, action, modifiers):
    # Key presses
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.SPACE:
                print(f"Current matrix:\n {self.generate_matrix()}")

            if key == self.wnd.keys.R:
                self.refresh()
            if key == self.wnd.keys.D:
                self.create_matrices()

            # Using modifiers (shift and ctrl)

            if key == self.wnd.keys.Z and modifiers.shift:
                print("Shift + Z was pressed")

            if key == self.wnd.keys.Z and modifiers.ctrl:
                print("ctrl + Z was pressed")

        # Key releases
        elif action == self.wnd.keys.ACTION_RELEASE:
            if key == self.wnd.keys.SPACE:
                print("SPACE key was released")

    def render(self, time: float, frame_time: float):
        self.refresh()
        self.ctx.clear(0.0, 0.0, 0.0)
        self.vao.render()


if __name__ == "__main__":
    FractalRenderer.run()