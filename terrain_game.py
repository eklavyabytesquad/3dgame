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
from components.coins import CoinManager
from components.obstacles import ObstacleManager

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
        
        # Game state
        self.is_alive = True
        self.game_over = False
        
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
        
        # Create coins to collect
        self.coins = CoinManager(self.loader, self.render)
        
        # Create dangerous obstacles (crabs)
        self.obstacles = ObstacleManager(self.loader, self.render)
        
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
        
        # Restart
        self.accept("r", self.restart_game)
        
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
        
        if not self.game_over:
            # Update player
            self.player.update(self.keys, dt)
            
            # Get player position
            player_pos = self.player.get_position()
            player_heading = self.player.get_heading()
            
            # Update coins (check for collection)
            self.coins.update(player_pos, dt)
            
            # Update obstacles and check collision
            hit_obstacle = self.obstacles.update(player_pos, dt)
            
            if hit_obstacle:
                self._handle_death()
            
            # Update camera
            self.camera_controller.update(player_pos, player_heading, dt)
            
            # Update UI
            self.ui.update_position(player_pos.x, player_pos.y, player_heading)
            self.ui.update_coins(self.coins.get_collected_count(), self.coins.get_total_coins())
            self.ui.update_health(self.is_alive)
        
        return task.cont
    
    def _handle_death(self):
        """Handle player death"""
        self.is_alive = False
        self.game_over = True
        coins_collected = self.coins.get_collected_count()
        self.ui.show_game_over(coins_collected)
        self.ui.update_health(False)
    
    def restart_game(self):
        """Restart the game"""
        if not self.game_over:
            return
        
        # Reset game state
        self.is_alive = True
        self.game_over = False
        
        # Reset player position
        self.player.model.setPos(50, 50, 2)
        self.player.position.set(50, 50, 2)
        self.player.heading = 0
        
        # Hide game over UI
        self.ui.hide_game_over()
        self.ui.update_health(True)

if __name__ == "__main__":
    game = TerrainExplorer()
    game.run()
