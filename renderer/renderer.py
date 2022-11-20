import numpy as np
import moderngl
import moderngl_window as mglw
from pathlib import Path
import pickle
from time import time


SHADER_ROOT = Path(__file__).parent / "shaders"
VERTEX_PATH = Path(__file__).parent / "vertices/vertices.pkl"
TRACE_VERTEX_SHADER = SHADER_ROOT / "trace_vertex_shader.glsl"
TRACE_FRAGMENT_SHADER = SHADER_ROOT / "trace_fragment_shader.glsl"
POSITION_VERTEX_SHADER = SHADER_ROOT / "position_vertex_shader.glsl"
POSITION_FRAGMENT_SHADER = SHADER_ROOT / "position_fragment_shader.glsl"

class WindowConf(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "ModernGL WindowConf"
    # window_size = (100, 100)
    window_size = (720, 720)
    aspect_ratio = 1
    # aspect_ratio = 16 / 9
    resizable = True


class RouteRenderer(WindowConf):
    title = "RouteRenderer"

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._last_vertex_update_time = 0
        self._last_shader_update_time = 0
        self.ctx.enable(moderngl.BLEND)
        self.init_time = time()
        self.matrices = {
            "translation": np.eye(4),
            "scale": np.eye(4),
            "rotation": np.eye(4),
        }
        self.refresh()

    def get_projection_matrix(self):
        T = time() - self.init_time
        scale = self.matrices["scale"].copy()
        scale[0, 0] = (0.7 + 0.3 * np.sin(T))
        scale[1, 1] = (0.7 + 0.3 * np.sin(1+T))
        translation = self.matrices["translation"].copy()
        return scale
        return np.matmul(
            scale,
            translation,
        )

    def generate_static_content(self):
        T = time() - self.init_time
        return [T, *self.get_projection_matrix().reshape((-1))]

    def read_shaders(self):
        def _read_shader_file(path):
            with open(path, "r") as f:
                return f.read()
        shader_path_dict = {
            "trace_fragment_shader": TRACE_FRAGMENT_SHADER,
            "trace_vertex_shader": TRACE_VERTEX_SHADER,
            "position_fragment_shader": POSITION_FRAGMENT_SHADER,
            "position_vertex_shader": POSITION_VERTEX_SHADER,
        }
        return {shader: _read_shader_file(shader_path) for shader, shader_path in shader_path_dict.items()}

    def reload_vertices(self):
        if VERTEX_PATH.stat().st_mtime > self._last_vertex_update_time:
            while True:
                try:
                    with open(VERTEX_PATH, "rb") as f:
                        self.trace_vertices, self.position_vertices = pickle.load(f)
                        break
                except Exception as e:
                    print(f"Failed to load! ({e})")
        return self.trace_vertices, self.position_vertices
    
    def shaders_need_reloading(self):
        current_shader_update_times = [glsl_file.stat().st_mtime for glsl_file in SHADER_ROOT.glob("*.glsl")]
        if any([update_time > self._last_shader_update_time for update_time in current_shader_update_times]):
            self._last_shader_update_time = max(current_shader_update_times)
            return True
        return False
            

    def refresh(self):
        if self.shaders_need_reloading():
            shader_dict = self.read_shaders()
            self.trace_prog = self.ctx.program(
                vertex_shader=shader_dict["trace_vertex_shader"],
                fragment_shader=shader_dict["trace_fragment_shader"],
            )
            self.position_prog = self.ctx.program(
                vertex_shader=shader_dict["position_vertex_shader"],
                fragment_shader=shader_dict["position_fragment_shader"],
            )        

        trace_vertices, position_vertices = self.reload_vertices()
        trace_vertices_bytes = np.array(trace_vertices, dtype="f4")
        position_vertices_bytes = np.array(position_vertices, dtype="f4")
        constant_objects_bytes = np.array(self.generate_static_content(), dtype="f4")

        self.trace_vbo = self.ctx.buffer(trace_vertices_bytes)
        self.position_vbo = self.ctx.buffer(position_vertices_bytes)
        self.constant_vbo = self.ctx.buffer(position_vertices_bytes)
        self.constant_objects_vbo = self.ctx.buffer(constant_objects_bytes)
        
        self.trace_vao = self.ctx.vertex_array(
            self.trace_prog,
            [
                (self.trace_vbo, '2f 2f 2f 1f 4f 4f', 'in_vert', 'in_ref_p0', 'in_ref_p1', 'in_width', 'in_color_p0', 'in_color_p1'),
                (self.constant_objects_vbo, '1f 16f /r', 'in_walltime', 'proj_mtx'),
            ],
        )
        
        self.position_vao = self.ctx.vertex_array(
            self.position_prog,
            [
                (self.position_vbo, '2f 1f 2f', 'in_vert', 'in_size', 'in_centroid'),
                (self.constant_objects_vbo, '1f 16f /r', 'in_walltime', 'proj_mtx'),
            ],
        )

        self._last_update_time = VERTEX_PATH.stat().st_mtime
        
        
    def render(self, time: float, frame_time: float):
        self.refresh()
        self.ctx.clear(0.0, 0.0, 0.0)
        self.trace_vao.render()
        self.position_vao.render()