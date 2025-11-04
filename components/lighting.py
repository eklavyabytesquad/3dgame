"""
Lighting component for atmospheric scene lighting
"""
from panda3d.core import AmbientLight, DirectionalLight, Vec4, PointLight

class LightingManager:
    def __init__(self, render):
        self.render = render
        self._setup_lights()
    
    def _setup_lights(self):
        """Create beautiful outdoor lighting"""
        # Ambient light (soft sky light)
        ambient = AmbientLight("ambient")
        ambient.setColor(Vec4(0.4, 0.45, 0.55, 1))  # Soft blue-ish
        self.ambient_np = self.render.attachNewNode(ambient)
        self.render.setLight(self.ambient_np)
        
        # Sun (main directional light)
        sun = DirectionalLight("sun")
        sun.setColor(Vec4(1, 0.95, 0.85, 1))  # Warm sunlight
        self.sun_np = self.render.attachNewNode(sun)
        self.sun_np.setHpr(120, -45, 0)  # Afternoon sun angle
        self.render.setLight(self.sun_np)
        
        # Secondary fill light (bounced light simulation)
        fill = DirectionalLight("fill")
        fill.setColor(Vec4(0.3, 0.35, 0.45, 1))  # Cool fill
        self.fill_np = self.render.attachNewNode(fill)
        self.fill_np.setHpr(-60, -20, 0)
        self.render.setLight(self.fill_np)
