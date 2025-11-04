"""
Coin/Cash collection system component
"""
import random
from panda3d.core import Vec3

class CoinManager:
    def __init__(self, loader, render):
        self.loader = loader
        self.render = render
        self.coins = []
        self.collected_count = 0
        self._spawn_coins()
    
    def _spawn_coins(self):
        """Spawn coins across the terrain"""
        num_coins = 50
        
        for i in range(num_coins):
            x = random.uniform(15, 185)
            y = random.uniform(15, 185)
            
            # Create coin
            coin = self._create_coin(x, y)
            
            self.coins.append({
                'model': coin,
                'position': Vec3(x, y, 3),
                'collected': False,
                'rotation': 0
            })
    
    def _create_coin(self, x, y):
        """Create a single coin model"""
        # Main coin body (flat cylinder look using box)
        coin_node = self.render.attachNewNode("coin")
        
        # Gold coin disc
        coin_disc = self.loader.loadModel("models/misc/sphere")
        coin_disc.setScale(0.6, 0.6, 0.15)
        coin_disc.setPos(0, 0, 0)  # Relative to coin_node
        coin_disc.setColor(1, 0.84, 0, 1)  # Gold color
        coin_disc.reparentTo(coin_node)
        
        # Inner circle for detail
        inner_circle = self.loader.loadModel("models/misc/sphere")
        inner_circle.setScale(0.45, 0.45, 0.16)
        inner_circle.setPos(0, 0, 0)  # Relative to coin_node
        inner_circle.setColor(1, 0.95, 0.3, 1)  # Lighter gold
        inner_circle.reparentTo(coin_node)
        
        # Dollar sign symbol (using boxes)
        # Vertical line
        v_line = self.loader.loadModel("models/box")
        v_line.setScale(0.08, 0.08, 0.5)
        v_line.setPos(0, 0, 0)  # Relative to coin_node
        v_line.setColor(0.6, 0.4, 0, 1)  # Dark gold
        v_line.reparentTo(coin_node)
        
        # S curve (simplified with boxes)
        s_top = self.loader.loadModel("models/box")
        s_top.setScale(0.25, 0.08, 0.1)
        s_top.setPos(0, 0, 0.15)  # Relative to coin_node
        s_top.setColor(0.6, 0.4, 0, 1)
        s_top.reparentTo(coin_node)
        
        s_bottom = self.loader.loadModel("models/box")
        s_bottom.setScale(0.25, 0.08, 0.1)
        s_bottom.setPos(0, 0, -0.15)  # Relative to coin_node
        s_bottom.setColor(0.6, 0.4, 0, 1)
        s_bottom.reparentTo(coin_node)
        
        # Glow effect
        glow = self.loader.loadModel("models/misc/sphere")
        glow.setScale(0.8, 0.8, 0.2)
        glow.setPos(0, 0, 0)  # Relative to coin_node
        glow.setColor(1, 1, 0.5, 0.3)
        glow.setTransparency(True)
        glow.reparentTo(coin_node)
        
        # Set the coin_node's position on terrain
        coin_node.setPos(x, y, 3)
        return coin_node
    
    def update(self, player_pos, dt):
        """Update coins (rotation and collection check)"""
        import math
        
        for coin_data in self.coins:
            if coin_data['collected']:
                continue
            
            # Rotate coin for visual effect (spin on Z axis)
            coin_data['rotation'] += 180 * dt
            coin_data['model'].setH(coin_data['rotation'])
            
            # Gentle bob up and down (stays near original position)
            bob = math.sin(coin_data['rotation'] * 0.05) * 0.3
            coin_pos = coin_data['position']
            
            # Keep coin at fixed X, Y position, only animate Z slightly
            coin_data['model'].setPos(coin_pos.x, coin_pos.y, coin_pos.z + bob)
            
            # Check if player is close enough to collect
            distance = self._distance_2d(player_pos, coin_pos)
            
            if distance < 2.5:  # Collection radius
                self._collect_coin(coin_data)
    
    def _distance_2d(self, pos1, pos2):
        """Calculate 2D distance between two positions"""
        import math
        dx = pos1.x - pos2.x
        dy = pos1.y - pos2.y
        return math.sqrt(dx * dx + dy * dy)
    
    def _collect_coin(self, coin_data):
        """Collect a coin"""
        coin_data['collected'] = True
        self.collected_count += 1
        
        # Animate collection (scale up and fade)
        coin_data['model'].setScale(1.5)
        
        # Remove from scene after a brief moment
        self._schedule_removal(coin_data['model'])
    
    def _schedule_removal(self, coin_model):
        """Schedule coin removal (simplified - immediate for now)"""
        # In a real game, you'd use a timed interval here
        # For now, hide it immediately
        coin_model.hide()
    
    def get_collected_count(self):
        """Get number of coins collected"""
        return self.collected_count
    
    def get_total_coins(self):
        """Get total number of coins"""
        return len(self.coins)
    
    def respawn_coin(self, index):
        """Respawn a specific coin (for endless gameplay)"""
        if index < len(self.coins):
            coin_data = self.coins[index]
            coin_data['collected'] = False
            coin_data['model'].show()
            coin_data['model'].setScale(1.0)
