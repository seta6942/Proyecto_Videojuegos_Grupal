"""
HUD: Sistema de interfaz de usuario, menús y notificaciones (Minimapa top-down real).
"""
import pygame
from src.settings import *

class HUD:
    def __init__(self, screen):
        self.screen = screen
        self.notifications = []
        
        self.font_title = pygame.font.SysFont('monospace', 48, bold=True)
        self.font_subtitle = pygame.font.SysFont('monospace', 22)
        self.font_large = pygame.font.SysFont('monospace', 36, bold=True)
        self.font_normal = pygame.font.SysFont('monospace', 20, bold=True)
        self.font_small = pygame.font.SysFont('monospace', 14)
        
        cx = SCREEN_WIDTH // 2
        cy = SCREEN_HEIGHT // 2
        self.btn_iniciar = pygame.Rect(cx - 125, cy - 10, 250, 50)
        self.btn_controles = pygame.Rect(cx - 125, cy + 60, 250, 50)
        self.btn_salir = pygame.Rect(cx - 125, cy + 130, 250, 50)
        
    def add_notification(self, text, color=(255, 255, 255), duration=3.0):
        self.notifications.append({'text': text, 'color': color, 'timer': duration})
        
    def update(self, dt, global_alert):
        for notif in self.notifications[:]:
            notif['timer'] -= dt
            if notif['timer'] <= 0:
                self.notifications.remove(notif)
                
    def draw(self, global_alert, player_stones, current_zone, fps, player_stamina, stone_cooldown=0.0, stone_cooldown_max=0.5):
        # 1. Barra de Alerta Global
        pygame.draw.rect(self.screen, (50, 0, 0), (20, 20, 200, 20))
        alert_width = (global_alert / ALERT_MAX) * 200
        color_alert = (255, 0, 0) if global_alert > ALERT_MAX * 0.7 else (255, 150, 0) if global_alert > ALERT_MAX * 0.3 else (0, 255, 0)
        pygame.draw.rect(self.screen, color_alert, (20, 20, alert_width, 20))
        pygame.draw.rect(self.screen, (255, 255, 255), (20, 20, 200, 20), 2)
        
        txt_alert = self.font_small.render(f"ALERTA: {int((global_alert/ALERT_MAX)*100)}%", True, (255, 255, 255))
        self.screen.blit(txt_alert, (25, 22))

        # 2. Barra de Estamina (NUEVO)
        pygame.draw.rect(self.screen, (0, 50, 50), (20, 50, 200, 15))
        stamina_width = (player_stamina / 100.0) * 200
        pygame.draw.rect(self.screen, (0, 255, 200), (20, 50, stamina_width, 15))
        pygame.draw.rect(self.screen, (255, 255, 255), (20, 50, 200, 15), 2)
        
        txt_stamina = self.font_small.render(f"ESTAMINA", True, (255, 255, 255))
        self.screen.blit(txt_stamina, (25, 50))
        
        # 3. Textos desplazados hacia abajo y Cooldown Visual
        txt_stones = self.font_normal.render(f"Piedras: {player_stones}", True, (200, 200, 200))
        self.screen.blit(txt_stones, (20, 75))
        
        # --- NUEVO: Indicador visual de cooldown ---
        icon_x = 20 + txt_stones.get_width() + 15
        icon_y = 75
        icon_size = 20
        
        # Fondo (vacío)
        pygame.draw.rect(self.screen, (50, 50, 50), (icon_x, icon_y, icon_size, icon_size), border_radius=3)
        
        if stone_cooldown > 0 and stone_cooldown_max > 0:
            fill_ratio = max(0.0, min(1.0, 1.0 - (stone_cooldown / stone_cooldown_max)))
            fill_h = int(icon_size * fill_ratio)
            if fill_h > 0:
                pygame.draw.rect(self.screen, (150, 150, 150), (icon_x, icon_y + icon_size - fill_h, icon_size, fill_h), border_radius=3)
        else:
            pygame.draw.rect(self.screen, (200, 200, 200), (icon_x, icon_y, icon_size, icon_size), border_radius=3)
            pygame.draw.circle(self.screen, (100, 100, 100), (icon_x + icon_size//2, icon_y + icon_size//2), icon_size//2 - 2)
            
        pygame.draw.rect(self.screen, (255, 255, 255), (icon_x, icon_y, icon_size, icon_size), 1, border_radius=3)
        # -------------------------------------------
        
        txt_zone = self.font_normal.render(f"Zona: {current_zone}", True, (150, 200, 255))
        self.screen.blit(txt_zone, (SCREEN_WIDTH - 150, 20))
        
        txt_fps = self.font_small.render(f"FPS: {int(fps)}", True, (100, 100, 100))
        self.screen.blit(txt_fps, (SCREEN_WIDTH - 80, 50))
        
        # 4. Notificaciones
        for i, notif in enumerate(self.notifications):
            alpha = min(255, int(notif['timer'] * 255))
            txt = self.font_normal.render(notif['text'], True, notif['color'])
            txt.set_alpha(alpha)
            self.screen.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2, 110 + i * 30))

    def draw_minimap(self, minimap_bg, map_w, map_h, player_pos, guards, exit_rect, scale=0.2):
        if not minimap_bg: return
        
        view_size = 250  # Tamaño de la ventana del minimapa
        margin = 20
        start_x = SCREEN_WIDTH - view_size - margin
        start_y = SCREEN_HEIGHT - view_size - margin
        
        # Borde exterior
        pygame.draw.rect(self.screen, (20, 20, 20), (start_x - 2, start_y - 2, view_size + 4, view_size + 4))
        
        # Coordenadas del jugador escaladas
        px_mini = int(player_pos[0] * scale)
        py_mini = int(player_pos[1] * scale)
        
        bg_w = minimap_bg.get_width()
        bg_h = minimap_bg.get_height()
        
        # Calcular el Viewport centrado en el jugador y limitar a los bordes del mapa
        view_x = px_mini - view_size // 2
        view_y = py_mini - view_size // 2
        view_x = max(0, min(view_x, bg_w - view_size))
        view_y = max(0, min(view_y, bg_h - view_size))
        
        actual_view_w = min(view_size, bg_w)
        actual_view_h = min(view_size, bg_h)
        view_rect = pygame.Rect(view_x, view_y, actual_view_w, actual_view_h)
        
        # Dibujar solo la porción visible (subsurface)
        self.screen.blit(minimap_bg, (start_x, start_y), view_rect)
        
        def get_minimap_pos(world_pos):
            mx = int(world_pos[0] * scale) - view_x
            my = int(world_pos[1] * scale) - view_y
            return start_x + mx, start_y + my
            
        if exit_rect:
            ex, ey = get_minimap_pos(exit_rect.center)
            if start_x <= ex <= start_x + view_size and start_y <= ey <= start_y + view_size:
                if pygame.time.get_ticks() % 1000 < 500:
                    pygame.draw.rect(self.screen, (0, 255, 0), (ex-4, ey-4, 8, 8))
                pygame.draw.rect(self.screen, (255, 255, 255), (ex-4, ey-4, 8, 8), 1)
            
        for guard in guards:
            gx, gy = get_minimap_pos(guard.pos)
            if start_x <= gx <= start_x + view_size and start_y <= gy <= start_y + view_size:
                if guard.state in ['chase', 'support']:
                    color = (255, 30, 30)
                elif guard.state == 'investigate':
                    color = (255, 220, 0)
                else:
                    color = (255, 120, 0)
                pygame.draw.circle(self.screen, color, (gx, gy), 3)
                
        px, py = get_minimap_pos(player_pos)
        pygame.draw.circle(self.screen, (0, 255, 255), (px, py), 4)
        pygame.draw.circle(self.screen, (255, 255, 255), (px, py), 4, 1)

        pygame.draw.rect(self.screen, (200, 200, 200), (start_x - 2, start_y - 2, view_size + 4, view_size + 4), 2)
        title = self.font_small.render("MINIMAPA", True, (200, 200, 200))
        self.screen.blit(title, (start_x, start_y - 20))

    def _draw_button(self, rect, text, mouse_pos):
        color_normal = (30, 40, 50)
        color_hover = (60, 80, 100)
        color_text = (200, 220, 255)
        
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, color_hover, rect, border_radius=5)
            pygame.draw.rect(self.screen, (100, 150, 255), rect, 2, border_radius=5)
        else:
            pygame.draw.rect(self.screen, color_normal, rect, border_radius=5)
            pygame.draw.rect(self.screen, (50, 70, 90), rect, 2, border_radius=5)
            
        img_text = self.font_normal.render(text, True, color_text)
        self.screen.blit(img_text, img_text.get_rect(center=rect.center))

    def draw_menu(self):
        self.screen.fill((10, 10, 15))
        mouse_pos = pygame.mouse.get_pos()
        
        title = self.font_title.render("SOMBRAS EN LA UNMSM", True, (255, 50, 50))
        subtitle = self.font_subtitle.render("INFILTRACION TACTICA NOCTURNA", True, (150, 150, 150))
        
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 120)))
        self.screen.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 70)))
        
        self._draw_button(self.btn_iniciar, "INICIAR", mouse_pos)
        self._draw_button(self.btn_controles, "CONTROLES", mouse_pos)
        self._draw_button(self.btn_salir, "SALIR", mouse_pos)

    def draw_controls(self):
        self.screen.fill((10, 10, 15))
        
        title = self.font_large.render("CONTROLES", True, (200, 200, 255))
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 100)))
        
        controls = [
            "W, A, S, D o Flechas : Moverse",
            "ESPACIO              : Ocultarse (Solo en Vegetación)",
            "CLIC DERECHO         : Lanzar piedra",
            "TECLA Q              : Activar alarma de auto",
            "ESC                  : Pausar juego"
        ]
        
        for i, text in enumerate(controls):
            txt = self.font_normal.render(text, True, (180, 180, 180))
            self.screen.blit(txt, (SCREEN_WIDTH//2 - 220, 200 + i * 40))
            
        volver = self.font_normal.render("Presiona ESC o HAZ CLIC para volver", True, (100, 100, 100))
        self.screen.blit(volver, volver.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 100)))

    def draw_game_over(self, reason):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((50, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        title = self.font_title.render("GAME OVER", True, (255, 50, 50))
        sub = self.font_large.render(reason, True, (200, 150, 150))
        restart = self.font_normal.render("Presiona 'R' para reiniciar", True, (255, 255, 255))
        
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50)))
        self.screen.blit(sub, sub.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 10)))
        self.screen.blit(restart, restart.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80)))
        
    def draw_win(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 50, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        title = self.font_title.render("¡ESCAPASTE!", True, (50, 255, 50))
        sub = self.font_normal.render("Lograste salir por la Puerta 7.", True, (200, 255, 200))
        
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20)))
        self.screen.blit(sub, sub.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30)))