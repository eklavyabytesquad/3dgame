"""
Tree generation component with realistic trees
"""
import random

class TreeManager:
    def __init__(self, loader, render):
        self.loader = loader
        self.render = render
        self.trees = []
        self._create_forest()
    
    def _create_forest(self):
        """Generate a forest of varied trees"""
        num_trees = 40
        
        for i in range(num_trees):
            x = random.uniform(10, 190)
            y = random.uniform(10, 190)
            
            # Don't spawn near center (player start)
            if abs(x - 50) < 15 and abs(y - 50) < 15:
                continue
            
            # Random tree type
            tree_type = random.choice(['pine', 'oak', 'birch'])
            
            if tree_type == 'pine':
                self._create_pine_tree(x, y)
            elif tree_type == 'oak':
                self._create_oak_tree(x, y)
            else:
                self._create_birch_tree(x, y)
            
            self.trees.append((x, y))
    
    def _create_pine_tree(self, x, y):
        """Create a pine/evergreen tree"""
        # Trunk
        trunk = self.loader.loadModel("models/box")
        trunk.setScale(0.6, 0.6, 6)
        trunk.setPos(x, y, 3)
        trunk.setColor(0.35, 0.25, 0.15, 1)  # Dark brown
        trunk.reparentTo(self.render)
        
        # Pine foliage layers (triangular shape)
        layer_heights = [4, 6, 8, 10]
        layer_scales = [5, 4, 3, 2]
        
        for height, scale in zip(layer_heights, layer_scales):
            layer = self.loader.loadModel("models/misc/sphere")
            layer.setScale(scale, scale, scale * 1.2)
            layer.setPos(x, y, height)
            
            # Dark green for pine
            g = random.uniform(0.3, 0.4)
            layer.setColor(0.1, g, 0.15, 1)
            layer.reparentTo(self.render)
    
    def _create_oak_tree(self, x, y):
        """Create a broad oak tree"""
        # Thick trunk
        trunk = self.loader.loadModel("models/box")
        trunk.setScale(0.9, 0.9, 5)
        trunk.setPos(x, y, 2.5)
        trunk.setColor(0.4, 0.3, 0.2, 1)  # Medium brown
        trunk.reparentTo(self.render)
        
        # Broad canopy (multiple spheres)
        canopy_positions = [
            (0, 0, 7),
            (-2, 1, 6.5),
            (2, -1, 6.5),
            (-1, -1.5, 7),
            (1.5, 1, 7),
        ]
        
        for dx, dy, dz in canopy_positions:
            foliage = self.loader.loadModel("models/misc/sphere")
            scale = random.uniform(2.5, 3.5)
            foliage.setScale(scale)
            foliage.setPos(x + dx, y + dy, dz)
            
            # Bright green for oak
            g = random.uniform(0.5, 0.7)
            foliage.setColor(0.15, g, 0.2, 1)
            foliage.reparentTo(self.render)
    
    def _create_birch_tree(self, x, y):
        """Create a tall birch tree"""
        # White/light trunk
        trunk = self.loader.loadModel("models/box")
        trunk.setScale(0.5, 0.5, 7)
        trunk.setPos(x, y, 3.5)
        trunk.setColor(0.9, 0.9, 0.85, 1)  # Light/white
        trunk.reparentTo(self.render)
        
        # Add dark stripes on trunk for birch look
        for i in range(4):
            stripe = self.loader.loadModel("models/box")
            stripe.setScale(0.55, 0.55, 0.4)
            stripe.setPos(x, y, 2 + i * 2)
            stripe.setColor(0.2, 0.2, 0.2, 1)
            stripe.reparentTo(self.render)
        
        # Light, airy canopy at top
        for i in range(3):
            foliage = self.loader.loadModel("models/misc/sphere")
            scale = random.uniform(2, 3)
            foliage.setScale(scale)
            
            dx = random.uniform(-1, 1)
            dy = random.uniform(-1, 1)
            foliage.setPos(x + dx, y + dy, 8 + i * 1.5)
            
            # Light green/yellow-green for birch
            g = random.uniform(0.65, 0.8)
            foliage.setColor(0.4, g, 0.3, 1)
            foliage.reparentTo(self.render)
    
    def get_tree_positions(self):
        """Return list of tree positions for collision detection"""
        return self.trees
