"""
Dangerous obstacles component (Crabs)
"""
import random
from panda3d.core import Vec3

class ObstacleManager:
    def __init__(self, loader, render):
        self.loader = loader
        self.render = render
        self.obstacles = []
        self._spawn_obstacles()
    
    def _spawn_obstacles(self):
        """Spawn dangerous crabs across terrain"""
        num_obstacles = 5  # Only 5 dangerous crabs
        
        for i in range(num_obstacles):
            x = random.uniform(20, 180)
            y = random.uniform(20, 180)
            
            # Don't spawn too close to player start
            if abs(x - 50) < 20 and abs(y - 50) < 20:
                continue
            
            # Create crab
            crab = self._create_crab(x, y)
            
            self.obstacles.append({
                'model': crab,
                'position': Vec3(x, y, 1),
                'animation_time': random.uniform(0, 360)
            })
    
    def _create_crab(self, x, y):
        """Create a dangerous crab model"""
        crab_node = self.render.attachNewNode("crab")
        
        # Body (main red shell)
        body = self.loader.loadModel("models/misc/sphere")
        body.setScale(1.2, 1.0, 0.6)
        body.setPos(0, 0, 0)
        body.setColor(0.9, 0.1, 0.1, 1)  # Bright red - danger!
        body.reparentTo(crab_node)
        
        # Eyes (stalks)
        left_eye_stalk = self.loader.loadModel("models/box")
        left_eye_stalk.setScale(0.1, 0.1, 0.4)
        left_eye_stalk.setPos(-0.6, -0.3, 0.5)
        left_eye_stalk.setColor(0.8, 0.1, 0.1, 1)
        left_eye_stalk.reparentTo(crab_node)
        
        right_eye_stalk = self.loader.loadModel("models/box")
        right_eye_stalk.setScale(0.1, 0.1, 0.4)
        right_eye_stalk.setPos(0.6, -0.3, 0.5)
        right_eye_stalk.setColor(0.8, 0.1, 0.1, 1)
        right_eye_stalk.reparentTo(crab_node)
        
        # Eyes
        left_eye = self.loader.loadModel("models/misc/sphere")
        left_eye.setScale(0.2)
        left_eye.setPos(-0.6, -0.3, 0.9)
        left_eye.setColor(1, 1, 0, 1)  # Yellow eyes
        left_eye.reparentTo(crab_node)
        
        right_eye = self.loader.loadModel("models/misc/sphere")
        right_eye.setScale(0.2)
        right_eye.setPos(0.6, -0.3, 0.9)
        right_eye.setColor(1, 1, 0, 1)
        right_eye.reparentTo(crab_node)
        
        # Claws (big and scary)
        left_claw_arm = self.loader.loadModel("models/box")
        left_claw_arm.setScale(0.3, 0.3, 0.8)
        left_claw_arm.setPos(-1.3, 0, 0.2)
        left_claw_arm.setColor(0.85, 0.15, 0.15, 1)
        left_claw_arm.reparentTo(crab_node)
        
        right_claw_arm = self.loader.loadModel("models/box")
        right_claw_arm.setScale(0.3, 0.3, 0.8)
        right_claw_arm.setPos(1.3, 0, 0.2)
        right_claw_arm.setColor(0.85, 0.15, 0.15, 1)
        right_claw_arm.reparentTo(crab_node)
        
        # Claw pincers
        left_claw = self.loader.loadModel("models/misc/sphere")
        left_claw.setScale(0.5, 0.4, 0.3)
        left_claw.setPos(-1.3, 0, 1.0)
        left_claw.setColor(1, 0.2, 0.2, 1)
        left_claw.reparentTo(crab_node)
        
        right_claw = self.loader.loadModel("models/misc/sphere")
        right_claw.setScale(0.5, 0.4, 0.3)
        right_claw.setPos(1.3, 0, 1.0)
        right_claw.setColor(1, 0.2, 0.2, 1)
        right_claw.reparentTo(crab_node)
        
        # Legs (6 small legs)
        for i in range(6):
            leg = self.loader.loadModel("models/box")
            leg.setScale(0.15, 0.15, 0.5)
            
            side = -1 if i < 3 else 1
            offset = (i % 3) * 0.4 - 0.4
            leg.setPos(side * 0.8, offset, -0.3)
            leg.setColor(0.7, 0.1, 0.1, 1)
            leg.reparentTo(crab_node)
        
        # Warning indicator (red glow)
        warning = self.loader.loadModel("models/misc/sphere")
        warning.setScale(2.0, 2.0, 0.3)
        warning.setPos(0, 0, 0)
        warning.setColor(1, 0, 0, 0.3)
        warning.setTransparency(True)
        warning.reparentTo(crab_node)
        
        # Danger symbol above (!)
        danger_mark = self.loader.loadModel("models/box")
        danger_mark.setScale(0.15, 0.15, 0.8)
        danger_mark.setPos(0, 0, 2.5)
        danger_mark.setColor(1, 1, 0, 1)
        danger_mark.reparentTo(crab_node)
        
        danger_dot = self.loader.loadModel("models/misc/sphere")
        danger_dot.setScale(0.2)
        danger_dot.setPos(0, 0, 1.8)
        danger_dot.setColor(1, 1, 0, 1)
        danger_dot.reparentTo(crab_node)
        
        crab_node.setPos(x, y, 1)
        return crab_node
    
    def update(self, player_pos, dt):
        """Update obstacles and check collision"""
        import math
        
        for obstacle in self.obstacles:
            # Animate crab (slight movement and rotation)
            obstacle['animation_time'] += dt * 100
            
            # Rock back and forth
            rock = math.sin(obstacle['animation_time'] * 0.05) * 5
            obstacle['model'].setH(rock)
            
            # Bob slightly
            bob = math.sin(obstacle['animation_time'] * 0.03) * 0.2
            obs_pos = obstacle['position']
            obstacle['model'].setPos(obs_pos.x, obs_pos.y, obs_pos.z + bob)
            
            # Check collision with player
            distance = self._distance_2d(player_pos, obs_pos)
            
            if distance < 3.0:  # Danger zone
                return True  # Player hit obstacle
        
        return False  # Safe
    
    def _distance_2d(self, pos1, pos2):
        """Calculate 2D distance"""
        import math
        dx = pos1.x - pos2.x
        dy = pos1.y - pos2.y
        return math.sqrt(dx * dx + dy * dy)
