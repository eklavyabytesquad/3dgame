"""
UI/HUD component for game interface
"""
from direct.gui.DirectGui import OnscreenText
from panda3d.core import TextNode

class GameUI:
    def __init__(self):
        self._create_ui()
    
    def _create_ui(self):
        """Create all UI elements with better design"""
        # Title with better styling
        self.title = OnscreenText(
            text="=== ADVENTURE WORLD ===",
            pos=(0, 0.92),
            scale=0.10,
            fg=(0.2, 1, 0.3, 1),
            align=TextNode.ACenter,
            shadow=(0, 0, 0, 1),
            shadowOffset=(0.02, 0.02)
        )
        
        # Controls info with better layout
        self.controls = OnscreenText(
            text="[WASD/ARROWS] Move  |  [COINS] Collect $  |  [AVOID] Red Crabs!  |  [ESC] Quit",
            pos=(0, -0.95),
            scale=0.048,
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter,
            shadow=(0, 0, 0, 0.8),
            shadowOffset=(0.015, 0.015)
        )
        
        # Coin wallet - styled as a panel
        self.coin_wallet = OnscreenText(
            text="",
            pos=(1.35, 0.88),
            scale=0.07,
            fg=(1, 0.84, 0, 1),
            align=TextNode.ARight,
            mayChange=True,
            shadow=(0.3, 0.2, 0, 1),
            shadowOffset=(0.02, 0.02)
        )
        
        # Health/Status indicator
        self.health_text = OnscreenText(
            text="STATUS: ALIVE",
            pos=(-1.35, 0.88),
            scale=0.06,
            fg=(0.3, 1, 0.3, 1),
            align=TextNode.ALeft,
            mayChange=True,
            shadow=(0, 0, 0, 1),
            shadowOffset=(0.02, 0.02)
        )
        
        # Position display - compact
        self.position_text = OnscreenText(
            text="",
            pos=(-1.35, 0.80),
            scale=0.05,
            fg=(0.8, 0.9, 1, 1),
            align=TextNode.ALeft,
            mayChange=True,
            shadow=(0, 0, 0, 0.8),
            shadowOffset=(0.015, 0.015)
        )
        
        # Game Over text (hidden initially)
        self.game_over_text = OnscreenText(
            text="",
            pos=(0, 0.1),
            scale=0.15,
            fg=(1, 0.2, 0.2, 1),
            align=TextNode.ACenter,
            mayChange=True,
            shadow=(0, 0, 0, 1),
            shadowOffset=(0.03, 0.03)
        )
        self.game_over_text.hide()
        
        # Restart instruction (hidden initially)
        self.restart_text = OnscreenText(
            text="",
            pos=(0, -0.1),
            scale=0.08,
            fg=(1, 1, 0.3, 1),
            align=TextNode.ACenter,
            mayChange=True,
            shadow=(0, 0, 0, 1),
            shadowOffset=(0.02, 0.02)
        )
        self.restart_text.hide()
    
    def update_position(self, x, y, heading):
        """Update position display"""
        self.position_text.setText(
            f"📍 Position: ({int(x)}, {int(y)})\n"
            f"🧭 Heading: {int(heading) % 360}°"
        )
    
    def update_coins(self, collected, total):
        """Update coin wallet display"""
        self.coin_wallet.setText(f"COINS: ${collected}/{total}")
    
    def show_game_over(self, coins_collected):
        """Show game over screen"""
        self.game_over_text.setText(
            f"=== GAME OVER ===\n\n"
            f"You were caught by a CRAB!\n"
            f"Coins Collected: ${coins_collected}"
        )
        self.game_over_text.show()
        
        self.restart_text.setText("Press [R] to Restart")
        self.restart_text.show()
    
    def hide_game_over(self):
        """Hide game over screen"""
        self.game_over_text.hide()
        self.restart_text.hide()
    
    def update_health(self, is_alive):
        """Update health status"""
        if is_alive:
            self.health_text.setText("STATUS: ALIVE")
            self.health_text.setFg((0.3, 1, 0.3, 1))
        else:
            self.health_text.setText("STATUS: DEAD")
            self.health_text.setFg((1, 0.2, 0.2, 1))
