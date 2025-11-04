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
        """Load 3D player model from OBJ file"""
        # Load the IronMan OBJ model
        try:
            player_model = self.loader.loadModel("components/IronMan.obj")
            if player_model:
                player_model.reparentTo(self.render)
                
                # Scale the model appropriately (making it smaller)
                player_model.setScale(0.01, 0.01, 0.01)
                
                # Stand the model upright (rotate 90 degrees on pitch)
                player_model.setP(90)  # Pitch to stand up
                player_model.setH(180)  # Face forward
                
                # Set color (red and gold for Iron Man!)
                player_model.setColor(0.9, 0.1, 0.1, 1)  # Red color
                
                # List all loaded nodes for debugging
                print("IronMan OBJ Model loaded successfully!")
                player_model.ls()
                
                return player_model
            else:
                print("OBJ model returned None")
                raise Exception("Model not loaded")
        except Exception as e:
            print(f"Error loading OBJ model: {e}")
            print("Using fallback sphere model")
            # Fallback to a simple sphere if OBJ fails to load
            fallback = self.loader.loadModel("models/misc/sphere")
            fallback.setScale(1.0)
            fallback.setColor(0.2, 0.4, 0.8, 1)
            fallback.reparentTo(self.render)
            return fallback
    
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
