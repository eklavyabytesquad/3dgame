"""
Camera controller for smooth third-person camera
"""
from panda3d.core import Vec3
import math

class CameraController:
    def __init__(self, camera):
        self.camera = camera
        self.distance = 15
        self.height = 8
        self.smoothness = 5.0
        self.target_pos = Vec3(0, 0, 0)
    
    def update(self, player_pos, player_heading, dt):
        """Smooth camera follow"""
        # Calculate desired camera position behind player
        rad = math.radians(player_heading)
        
        cam_x = player_pos.x - math.sin(rad) * self.distance
        cam_y = player_pos.y - math.cos(rad) * self.distance
        cam_z = player_pos.z + self.height
        
        # Smooth interpolation
        current_pos = self.camera.getPos()
        new_x = current_pos.x + (cam_x - current_pos.x) * self.smoothness * dt
        new_y = current_pos.y + (cam_y - current_pos.y) * self.smoothness * dt
        new_z = current_pos.z + (cam_z - current_pos.z) * self.smoothness * dt
        
        self.camera.setPos(new_x, new_y, new_z)
        
        # Look at player (slightly above center)
        look_at_pos = Vec3(player_pos.x, player_pos.y, player_pos.z + 2)
        self.camera.lookAt(look_at_pos)
