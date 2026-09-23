import os
import glfw
from OpenGL.GL import *
from PIL import Image

TILE_SIZE = 64

class TilePlayer:
    def __init__(self, config, script_path="scene.txt"):
        self.config = config
        self.script_path = script_path
        self.window = None
        self.loaded_textures = {}
        
        self.window_width = self.config.cols * TILE_SIZE
        self.window_height = self.config.rows * TILE_SIZE

    def _load_texture(self, image_path):
        """Загрузка текстуры в OpenGL"""
        try:
            img = Image.open(image_path).transpose(Image.FLIP_TOP_BOTTOM)
            img_data = img.convert("RGBA").tobytes()
            width, height = img.size
        except Exception as e:
            print(f" Не удалось загрузить текстуру '{image_path}': {e}")
            return None

        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        return tex_id

    def _init_gl(self):
        """Иницилализация GLFW"""
        if not glfw.init():
            raise RuntimeError("Не удалось инициализировать GLFW")

        self.window = glfw.create_window(
            self.window_width, 
            self.window_height, 
            "DSL Tilemap Player ", 
            None, 
            None
        )
        
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Не удалось создать окно GLFW")

        glfw.make_context_current(self.window)

        # Ортографическая 2D-проекция
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.window_width, self.window_height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Загрузка текстур
        script_dir = os.path.dirname(os.path.abspath(self.script_path))

        for tile_id, path in self.config.tiles.items():
            if not os.path.isabs(path):
                path = os.path.join(script_dir, path)

            self.loaded_textures[tile_id] = self._load_texture(path)

    def _draw_tile(self, x, y, size, tex_id):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex_id)


        
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex2f(x, y)
        glTexCoord2f(1.0, 1.0); glVertex2f(x + size, y)
        glTexCoord2f(1.0, 0.0); glVertex2f(x + size, y + size)
        glTexCoord2f(0.0, 0.0); glVertex2f(x, y + size)
        glEnd()

        glDisable(GL_TEXTURE_2D)

    def run(self):
        """Запуск отображения изображения"""
        self._init_gl()

        while not glfw.window_should_close(self.window):
            if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
                glfw.set_window_should_close(self.window, True)
                
            glClearColor(0.1, 0.1, 0.1, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)
            

            for r in range(self.config.rows):
                for c in range(self.config.cols):
                    tile_id = self.config.grid[r][c]
                    tex_id = self.loaded_textures.get(tile_id)
                    if tex_id:
                        self._draw_tile(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, tex_id)

            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glfw.terminate()