"""
UI/HUD component for game interface
"""
from direct.gui.DirectGui import OnscreenText
from panda3d.core import TextNode

class GameUI:
    def __init__(self):
        self._create_ui()
    
    def _create_ui(self):
        """Create all UI elements"""
        # Title
        self.title = OnscreenText(
            text="🌲 3D WORLD EXPLORER 🌲",
            pos=(0, 0.92),
            scale=0.09,
            fg=(1, 0.9, 0.3, 1),
            align=TextNode.ACenter,
            shadow=(0.3, 0.3, 0.3, 1)
        )
        
        # Controls info
        self.controls = OnscreenText(
            text="WASD or Arrow Keys = Move  •  Mouse = Look Around  •  ESC = Quit",
            pos=(0, -0.95),
            scale=0.05,
            fg=(0.9, 0.9, 1, 1),
            align=TextNode.ACenter,
            shadow=(0.1, 0.1, 0.1, 1)
        )
        
        # Position display
        self.position_text = OnscreenText(
            text="",
            pos=(-1.3, 0.85),
            scale=0.055,
            fg=(1, 1, 1, 1),
            align=TextNode.ALeft,
            mayChange=True,
            shadow=(0.1, 0.1, 0.1, 1)
        )
        
        # Speed/activity display
        self.status_text = OnscreenText(
            text="",
            pos=(1.3, 0.85),
            scale=0.055,
            fg=(0.4, 1, 0.4, 1),
            align=TextNode.ARight,
            mayChange=True,
            shadow=(0.1, 0.1, 0.1, 1)
        )
    
    def update_position(self, x, y, heading):
        """Update position display"""
        self.position_text.setText(
            f"📍 Position: ({int(x)}, {int(y)})\n"
            f"🧭 Heading: {int(heading) % 360}°"
        )
    
    def update_status(self, is_moving):
        """Update status display"""
        if is_moving:
            self.status_text.setText("🏃 Moving")
        else:
            self.status_text.setText("🧍 Standing")
