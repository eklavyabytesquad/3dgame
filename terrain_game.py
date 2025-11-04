from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import OnscreenText
from panda3d.core import AmbientLight, DirectionalLight, Vec3, Vec4, TextNode, PointLight, Fog
from panda3d.core import GeoMipTerrain, Filename
import random
import sys

class TerrainExplorer(ShowBase):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.disableMouse()
        self.setBackgroundColor(0.53, 0.81, 0.92, 1)  # Sky blue
        
        # Player variables
        self.player_pos = Vec3(50, 50, 0)
        self.player_heading = 0
        self.move_speed = 15.0
        self.turn_speed = 100.0
        
        # Movement keys state
        self.keys = {
            'forward': False,
            'backward': False,
            'left': False,
            'right': False
        }
        
        # Setup scene
        self.setup_camera()
        self.setup_lights()
        self.setup_fog()
        self.setup_player()
        self.setup_terrain()
        self.setup_trees()
        self.setup_ui()
        
        # Input
        self.setup_input()
        
        # Game loop
        self.taskMgr.add(self.update, "update")
    
    def setup_camera(self):
        """Third-person camera behind player"""
        self.camera.setPos(0, -15, 8)
        self.camera.lookAt(0, 0, 2)
    
    def setup_lights(self):
        """Add natural outdoor lighting"""
        # Ambient light (sky light)
        ambient = AmbientLight("ambient")
        ambient.setColor(Vec4(0.5, 0.5, 0.6, 1))
        ambient_np = self.render.attachNewNode(ambient)
        self.render.setLight(ambient_np)
        
        # Directional light (sun)
        sun = DirectionalLight("sun")
        sun.setColor(Vec4(1, 0.95, 0.8, 1))
        sun_np = self.render.attachNewNode(sun)
        sun_np.setHpr(45, -60, 0)
        self.render.setLight(sun_np)
    
    def setup_fog(self):
        """Add atmospheric fog for distant terrain"""
        fog = Fog("fog")
        fog.setColor(0.53, 0.81, 0.92)
        fog.setExpDensity(0.005)
        self.render.setFog(fog)
    
    def setup_player(self):
        """Create the player character (red ball)"""
        self.player = self.loader.loadModel("models/misc/sphere")
        self.player.setScale(1.5)
        self.player.setColor(1, 0.2, 0.2, 1)
        self.player.reparentTo(self.render)
        self.player.setPos(self.player_pos)
        
        # Add a marker/flag on player
        marker = self.loader.loadModel("models/box")
        marker.setScale(0.3, 0.3, 2)
        marker.setPos(0, 0, 3)
        marker.setColor(1, 1, 0, 1)
        marker.reparentTo(self.player)
    
    def setup_terrain(self):
        """Create procedural terrain"""
        # Create a simple flat terrain with some elevation
        self.terrain_node = self.render.attachNewNode("terrain")
        
        # Create ground tiles with slight variation
        tile_size = 10
        num_tiles = 20
        
        for x in range(num_tiles):
            for y in range(num_tiles):
                tile = self.loader.loadModel("models/box")
                tile.setScale(tile_size, tile_size, 0.5)
                
                # Random height variation
                height = random.uniform(-0.5, 1.0)
                tile.setPos(x * tile_size, y * tile_size, height)
                
                # Random green shades for grass
                green = random.uniform(0.3, 0.5)
                tile.setColor(0.2, green, 0.2, 1)
                tile.reparentTo(self.terrain_node)
        
        # Add some hills
        for i in range(8):
            hill = self.loader.loadModel("models/misc/sphere")
            hill.setScale(random.uniform(8, 15))
            x = random.uniform(20, 180)
            y = random.uniform(20, 180)
            hill.setPos(x, y, -5)
            hill.setColor(0.25, random.uniform(0.4, 0.6), 0.25, 1)
            hill.reparentTo(self.terrain_node)
    
    def setup_trees(self):
        """Create trees scattered around the terrain"""
        self.trees = []
        num_trees = 30
        
        for i in range(num_trees):
            # Avoid spawning too close to player start
            x = random.uniform(10, 190)
            y = random.uniform(10, 190)
            
            if abs(x - 50) < 10 and abs(y - 50) < 10:
                continue
            
            # Tree trunk
            trunk = self.loader.loadModel("models/box")
            trunk.setScale(0.8, 0.8, 5)
            trunk.setPos(x, y, 2.5)
            trunk.setColor(0.4, 0.25, 0.15, 1)
            trunk.reparentTo(self.render)
            
            # Tree foliage (multiple layers for volume)
            for layer in range(3):
                foliage = self.loader.loadModel("models/misc/sphere")
                scale = 3.5 - layer * 0.5
                foliage.setScale(scale)
                foliage.setPos(x, y, 6 + layer * 2)
                foliage.setColor(0.1, random.uniform(0.5, 0.7), 0.1, 1)
                foliage.reparentTo(self.render)
            
            self.trees.append((x, y))
    
    def setup_ui(self):
        """Create UI elements"""
        self.info_text = OnscreenText(
            text="🎮 W/S = Move  |  A/D = Turn  |  Arrow Keys = Move  |  ESC = Quit",
            pos=(0, -0.95),
            scale=0.05,
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter
        )
        
        self.position_text = OnscreenText(
            text="",
            pos=(-1.3, 0.9),
            scale=0.05,
            fg=(1, 1, 1, 1),
            align=TextNode.ALeft,
            mayChange=True
        )
        
        self.title_text = OnscreenText(
            text="🌲 3D TERRAIN EXPLORER 🌲",
            pos=(0, 0.9),
            scale=0.08,
            fg=(1, 1, 0, 1),
            align=TextNode.ACenter
        )
    
    def setup_input(self):
        """Setup keyboard controls"""
        # Movement
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
        
        # Quit
        self.accept("escape", sys.exit)
    
    def set_key(self, key, value):
        """Track key states"""
        self.keys[key] = value
    
    def update(self, task):
        """Main game loop"""
        dt = globalClock.getDt()
        if dt > 0.1:
            dt = 0.1
        
        # Handle rotation
        if self.keys['left']:
            self.player_heading += self.turn_speed * dt
        if self.keys['right']:
            self.player_heading -= self.turn_speed * dt
        
        # Handle movement
        move_x = 0
        move_y = 0
        
        if self.keys['forward']:
            move_y = self.move_speed * dt
        if self.keys['backward']:
            move_y = -self.move_speed * dt
        
        # Apply rotation to movement
        import math
        rad = math.radians(self.player_heading)
        dx = move_y * math.sin(rad)
        dy = move_y * math.cos(rad)
        
        # Update player position
        self.player_pos.x += dx
        self.player_pos.y += dy
        
        # Keep player in bounds
        self.player_pos.x = max(5, min(195, self.player_pos.x))
        self.player_pos.y = max(5, min(195, self.player_pos.y))
        
        # Simple terrain height (keep player slightly above ground)
        self.player_pos.z = 2
        
        # Update player transform
        self.player.setPos(self.player_pos)
        self.player.setH(self.player_heading)
        
        # Make player bob slightly when moving
        if self.keys['forward'] or self.keys['backward']:
            bob = math.sin(task.time * 8) * 0.3
            self.player.setZ(self.player_pos.z + bob)
        
        # Camera follows player (third-person)
        cam_x = self.player_pos.x - math.sin(rad) * 15
        cam_y = self.player_pos.y - math.cos(rad) * 15
        cam_z = self.player_pos.z + 8
        
        self.camera.setPos(cam_x, cam_y, cam_z)
        self.camera.lookAt(self.player_pos.x, self.player_pos.y, self.player_pos.z + 2)
        
        # Update UI
        self.position_text.setText(
            f"Position: ({int(self.player_pos.x)}, {int(self.player_pos.y)})\n"
            f"Heading: {int(self.player_heading) % 360}°"
        )
        
        return task.cont

if __name__ == "__main__":
    game = TerrainExplorer()
    game.run()
