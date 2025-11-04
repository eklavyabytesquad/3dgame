"""
Player character component with humanoid model
"""
from panda3d.core import Vec3
import math

class Player:
    def __init__(self, loader, render, start_pos=Vec3(50, 50, 2)):
        self.loader = loader
        self.render = render
        self.position = start_pos
        self.heading = 0
        self.move_speed = 20.0
        self.turn_speed = 120.0
        
        # Create player model
        self.model = self._create_player_model()
        self.model.setPos(self.position)
    
    def _create_player_model(self):
        """Create a humanoid character model"""
        # Main container
        player_node = self.render.attachNewNode("player")
        
        # Legs (bottom)
        left_leg = self.loader.loadModel("models/box")
        left_leg.setScale(0.4, 0.4, 1.2)
        left_leg.setPos(-0.4, 0, 0.6)
        left_leg.setColor(0.3, 0.3, 0.3, 1)  # Dark pants
        left_leg.reparentTo(player_node)
        
        right_leg = self.loader.loadModel("models/box")
        right_leg.setScale(0.4, 0.4, 1.2)
        right_leg.setPos(0.4, 0, 0.6)
        right_leg.setColor(0.3, 0.3, 0.3, 1)
        right_leg.reparentTo(player_node)
        
        # Feet
        left_foot = self.loader.loadModel("models/box")
        left_foot.setScale(0.4, 0.6, 0.2)
        left_foot.setPos(-0.4, 0.15, 0)
        left_foot.setColor(0.2, 0.2, 0.2, 1)
        left_foot.reparentTo(player_node)
        
        right_foot = self.loader.loadModel("models/box")
        right_foot.setScale(0.4, 0.6, 0.2)
        right_foot.setPos(0.4, 0.15, 0)
        right_foot.setColor(0.2, 0.2, 0.2, 1)
        right_foot.reparentTo(player_node)
        
        # Body (torso) - centered above legs
        body = self.loader.loadModel("models/box")
        body.setScale(1.0, 0.6, 1.4)
        body.setPos(0, 0, 2.1)
        body.setColor(0.2, 0.4, 0.8, 1)  # Blue shirt
        body.reparentTo(player_node)
        
        # Neck
        neck = self.loader.loadModel("models/box")
        neck.setScale(0.3, 0.3, 0.3)
        neck.setPos(0, 0, 2.95)
        neck.setColor(0.95, 0.8, 0.7, 1)  # Skin tone
        neck.reparentTo(player_node)
        
        # Head - directly above body
        head = self.loader.loadModel("models/misc/sphere")
        head.setScale(0.6)
        head.setPos(0, 0, 3.5)
        head.setColor(0.95, 0.8, 0.7, 1)  # Skin tone
        head.reparentTo(player_node)
        
        # Eyes
        left_eye = self.loader.loadModel("models/misc/sphere")
        left_eye.setScale(0.12)
        left_eye.setPos(-0.2, -0.55, 3.55)
        left_eye.setColor(1, 1, 1, 1)
        left_eye.reparentTo(player_node)
        
        right_eye = self.loader.loadModel("models/misc/sphere")
        right_eye.setScale(0.12)
        right_eye.setPos(0.2, -0.55, 3.55)
        right_eye.setColor(1, 1, 1, 1)
        right_eye.reparentTo(player_node)
        
        # Pupils
        left_pupil = self.loader.loadModel("models/misc/sphere")
        left_pupil.setScale(0.06)
        left_pupil.setPos(-0.2, -0.63, 3.55)
        left_pupil.setColor(0.1, 0.1, 0.1, 1)
        left_pupil.reparentTo(player_node)
        
        right_pupil = self.loader.loadModel("models/misc/sphere")
        right_pupil.setScale(0.06)
        right_pupil.setPos(0.2, -0.63, 3.55)
        right_pupil.setColor(0.1, 0.1, 0.1, 1)
        right_pupil.reparentTo(player_node)
        
        # Smile
        mouth = self.loader.loadModel("models/box")
        mouth.setScale(0.25, 0.05, 0.05)
        mouth.setPos(0, -0.58, 3.25)
        mouth.setColor(0.8, 0.3, 0.3, 1)
        mouth.reparentTo(player_node)
        
        # Arms - attached to body
        left_arm = self.loader.loadModel("models/box")
        left_arm.setScale(0.3, 0.3, 1.1)
        left_arm.setPos(-0.9, 0, 2.1)
        left_arm.setColor(0.2, 0.4, 0.8, 1)
        left_arm.reparentTo(player_node)
        
        right_arm = self.loader.loadModel("models/box")
        right_arm.setScale(0.3, 0.3, 1.1)
        right_arm.setPos(0.9, 0, 2.1)
        right_arm.setColor(0.2, 0.4, 0.8, 1)
        right_arm.reparentTo(player_node)
        
        # Hands
        left_hand = self.loader.loadModel("models/misc/sphere")
        left_hand.setScale(0.25)
        left_hand.setPos(-0.9, 0, 1.25)
        left_hand.setColor(0.95, 0.8, 0.7, 1)
        left_hand.reparentTo(player_node)
        
        right_hand = self.loader.loadModel("models/misc/sphere")
        right_hand.setScale(0.25)
        right_hand.setPos(0.9, 0, 1.25)
        right_hand.setColor(0.95, 0.8, 0.7, 1)
        right_hand.reparentTo(player_node)
        
        # Hat/cap for style
        hat = self.loader.loadModel("models/box")
        hat.setScale(0.7, 0.7, 0.25)
        hat.setPos(0, 0, 4.0)
        hat.setColor(0.8, 0.1, 0.1, 1)  # Red cap
        hat.reparentTo(player_node)
        
        return player_node
    
    def update(self, keys, dt):
        """Update player position and rotation"""
        # Handle rotation
        if keys['left']:
            self.heading += self.turn_speed * dt
        if keys['right']:
            self.heading -= self.turn_speed * dt
        
        # Handle movement
        move_distance = 0
        if keys['forward']:
            move_distance = self.move_speed * dt
        if keys['backward']:
            move_distance = -self.move_speed * dt
        
        # Apply movement with rotation
        if move_distance != 0:
            rad = math.radians(self.heading)
            dx = move_distance * math.sin(rad)
            dy = move_distance * math.cos(rad)
            
            self.position.x += dx
            self.position.y += dy
            
            # Keep in bounds
            self.position.x = max(5, min(195, self.position.x))
            self.position.y = max(5, min(195, self.position.y))
            
            # Walking animation (bob)
            bob = math.sin(dt * 50) * 0.2
            self.model.setZ(self.position.z + bob)
        
        # Update transform
        self.model.setPos(self.position.x, self.position.y, self.position.z)
        self.model.setH(self.heading)
    
    def get_position(self):
        """Get current position"""
        return self.position
    
    def get_heading(self):
        """Get current heading"""
        return self.heading
