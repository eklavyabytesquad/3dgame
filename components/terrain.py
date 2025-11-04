"""
Terrain generation component with varied landscape
"""
import random
from panda3d.core import Vec3

class Terrain:
    def __init__(self, loader, render):
        self.loader = loader
        self.render = render
        self.terrain_node = render.attachNewNode("terrain")
        self._create_terrain()
    
    def _create_terrain(self):
        """Generate beautiful varied terrain"""
        tile_size = 10
        num_tiles = 20
        
        # Create ground with color variation
        for x in range(num_tiles):
            for y in range(num_tiles):
                tile = self.loader.loadModel("models/box")
                tile.setScale(tile_size, tile_size, 0.3)
                
                # Varied height for natural look
                height = random.uniform(-0.3, 0.5)
                
                # Use Perlin-like noise for more natural variation
                noise = (x % 3) * 0.2 + (y % 3) * 0.2
                height += noise
                
                tile.setPos(x * tile_size, y * tile_size, height)
                
                # Rich grass colors with variation
                r = random.uniform(0.15, 0.25)
                g = random.uniform(0.45, 0.65)
                b = random.uniform(0.15, 0.25)
                tile.setColor(r, g, b, 1)
                tile.reparentTo(self.terrain_node)
        
        # Add rolling hills for depth
        self._create_hills()
        
        # Add paths/trails
        self._create_paths()
        
        # Add flowers/grass patches
        self._create_vegetation_patches()
    
    def _create_hills(self):
        """Create rolling hills"""
        for i in range(12):
            hill = self.loader.loadModel("models/misc/sphere")
            scale = random.uniform(6, 18)
            hill.setScale(scale, scale, scale * 0.4)
            
            x = random.uniform(15, 185)
            y = random.uniform(15, 185)
            hill.setPos(x, y, -scale * 0.3)
            
            # Grass color for hills
            r = random.uniform(0.2, 0.3)
            g = random.uniform(0.5, 0.7)
            b = random.uniform(0.2, 0.3)
            hill.setColor(r, g, b, 1)
            hill.reparentTo(self.terrain_node)
    
    def _create_paths(self):
        """Create dirt paths across terrain"""
        # Horizontal path
        for i in range(20):
            path = self.loader.loadModel("models/box")
            path.setScale(10, 4, 0.1)
            path.setPos(i * 10, 100, 0.6)
            path.setColor(0.6, 0.5, 0.3, 1)  # Dirt brown
            path.reparentTo(self.terrain_node)
        
        # Vertical path
        for i in range(20):
            path = self.loader.loadModel("models/box")
            path.setScale(4, 10, 0.1)
            path.setPos(100, i * 10, 0.6)
            path.setColor(0.6, 0.5, 0.3, 1)
            path.reparentTo(self.terrain_node)
    
    def _create_vegetation_patches(self):
        """Add small vegetation details"""
        for i in range(40):
            # Flower patches
            patch = self.loader.loadModel("models/misc/sphere")
            patch.setScale(random.uniform(0.3, 0.8))
            
            x = random.uniform(10, 190)
            y = random.uniform(10, 190)
            patch.setPos(x, y, 1.5)
            
            # Random flower colors
            colors = [
                (1, 0.3, 0.3, 1),  # Red
                (1, 1, 0.3, 1),    # Yellow
                (0.8, 0.3, 1, 1),  # Purple
                (1, 0.6, 0.8, 1),  # Pink
            ]
            patch.setColor(random.choice(colors))
            patch.reparentTo(self.terrain_node)
