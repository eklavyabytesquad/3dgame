"""
3D Terrain Explorer - Main Game
A beautiful 3D world with terrain, trees, and character exploration
"""
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Fog
import sys

# Import our components
from components.player import Player
from components.terrain import Terrain
from components.trees import TreeManager
from components.lighting import LightingManager
from components.camera import CameraController
from components.ui import GameUI

class TerrainExplorer(ShowBase):
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.disableMouse()
        self.setBackgroundColor(0.53, 0.81, 0.92, 1)  # Beautiful sky blue
        
        # Movement state
        self.keys = {
            'forward': False,
            'backward': False,
            'left': False,
            'right': False
        }
        
        # Initialize components
        self._init_scene()
        self._init_input()
        
        # Start game loop
        self.taskMgr.add(self.update, "update")
    
    def _init_scene(self):
        """Initialize all scene components"""
        # Lighting first for proper rendering
        self.lighting = LightingManager(self.render)
        
        # Add atmospheric fog
        self._setup_fog()
        
        # Create terrain
        self.terrain = Terrain(self.loader, self.render)
        
        # Create trees
        self.trees = TreeManager(self.loader, self.render)
        
        # Create player character
        self.player = Player(self.loader, self.render)
        
        # Setup camera controller
        self.camera_controller = CameraController(self.camera)
        
        # Create UI
        self.ui = GameUI()
    
    def _setup_fog(self):
        """Add atmospheric fog for depth"""
        fog = Fog("scene_fog")
        fog.setColor(0.53, 0.81, 0.92)
        fog.setExpDensity(0.004)
        self.render.setFog(fog)
    
    def _init_input(self):
        """Setup keyboard controls"""
        # WASD keys
        self.accept("w", self.set_key, ['forward', True])
        self.accept("w-up", self.set_key, ['forward', False])
        self.accept("s", self.set_key, ['backward', True])
        self.accept("s-up", self.set_key, ['backward', False])
        self.accept("a", self.set_key, ['left', True])
        self.accept("a-up", self.set_key, ['left', False])
        self.accept("d", self.set_key, ['right', True])
        self.accept("d-up", self.set_key, ['right', False])
        
        # Arrow keys
        self.accept("arrow_up", self.set_key, ['forward', True])
        self.accept("arrow_up-up", self.set_key, ['forward', False])
        self.accept("arrow_down", self.set_key, ['backward', True])
        self.accept("arrow_down-up", self.set_key, ['backward', False])
        self.accept("arrow_left", self.set_key, ['left', True])
        self.accept("arrow_left-up", self.set_key, ['left', False])
        self.accept("arrow_right", self.set_key, ['right', True])
        self.accept("arrow_right-up", self.set_key, ['right', False])
        
        # Exit
        self.accept("escape", sys.exit)
    
    def set_key(self, key, value):
        """Update key state"""
        self.keys[key] = value
    
    def update(self, task):
        """Main game loop"""
        dt = globalClock.getDt()
        if dt > 0.1:
            dt = 0.1
        
        # Update player
        self.player.update(self.keys, dt)
        
        # Update camera
        player_pos = self.player.get_position()
        player_heading = self.player.get_heading()
        self.camera_controller.update(player_pos, player_heading, dt)
        
        # Update UI
        is_moving = any([self.keys['forward'], self.keys['backward']])
        self.ui.update_position(player_pos.x, player_pos.y, player_heading)
        self.ui.update_status(is_moving)
        
        return task.cont

if __name__ == "__main__":
    game = TerrainExplorer()
    game.run()
