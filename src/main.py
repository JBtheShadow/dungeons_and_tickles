from __future__ import annotations

import sys
import pygame
from job import JOBS

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Callable

WIN_WIDTH = 1280
WIN_HEIGHT = 720

ALIGN_LEFT = 0x01
ALIGN_CENTER = 0x02
ALIGN_RIGHT = 0x04
VALIGN_TOP = 0x08
VALIGN_CENTER = 0x10
VALIGN_BOTTOM = 0x20

CURSOR_NONE = ''
CURSOR_EMPTY = ' '
CURSOR_FULL = '■'


def quit_to_desktop():
    pygame.event.post(pygame.event.Event(pygame.QUIT, {}))

def draw_text(win: pygame.Surface, text: Text):
    bounds = text.bounds()

    color = text.color
    if text.hover_color:
        x, y = pygame.mouse.get_pos()
        if bounds.left <= x <= bounds.right and bounds.top <= y <= bounds.bottom:
            color = text.hover_color

    if isinstance(text.text, list):
        text_surf = pygame.Surface((bounds.width, bounds.height))
        offset_y = 0
        step_y = int(text.font.get_linesize() * 1.4)
        for item in text.text:
            t_surf = text.font.render(item, True, color)
            t_rect = t_surf.get_rect()
            if text.align & ALIGN_CENTER:
                t_rect.centerx = bounds.width // 2
            elif text.align & ALIGN_RIGHT:
                t_rect.right = bounds.width
            t_rect.top = offset_y
            offset_y += step_y
            text_surf.blit(t_surf, t_rect)
    else:
        text_surf = text.font.render(text.text, True, color)
    
    win.blit(text_surf, bounds)

def change_player_count(state: GameState, value):
    state.player_count += value
    state.player_count = max(1, min(state.player_count, 6))

def change_player_job(state: GameState, value):
    player = state.players[state.current_player]
    i = list(JOBS).index(player.job) + value
    if i < 0:
        i = len(JOBS) - 1
    elif i >= len(JOBS):
        i = 0
    player.job = list(JOBS)[i]

def change_screen(state, screen):
    if screen == 'player_count':
        if state.screen == 'title':
            state.player_count = 1
    if screen == 'player_setup':
        state.current_player = 0
        state.players = [Player(f'Player {i}', 'warrior') for i in range(1, state.player_count + 1)]
    state.screen = screen

def setup_next_player(state: GameState, next):
    state.current_player += next
    if state.current_player < 0:
        change_screen(state, 'player_count')
        return
    elif state.current_player >= state.player_count:
        state.current_player = state.player_count - 1
        # next screen
        return

def keyboard_input(event, obj, field):
    if event.key == pygame.K_BACKSPACE:
        setattr(obj, field, getattr(obj, field)[:-1])
    elif event.unicode:
        setattr(obj, field, getattr(obj, field) + event.unicode)


class Text:
    def __init__(self,
                 text: str | list[str],
                 x: int,
                 y: int,
                 font: pygame.font.Font,
                 align: int = ALIGN_LEFT,
                 color: str | tuple[int, int, int] = 'white',
                 hover_color: str | tuple[int, int, int] = None):
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.align = align
        self.color = color
        self.hover_color = hover_color

    def size(self) -> tuple[int, int]:
        if isinstance(self.text, list):
            sizes = [self.font.size(text) for text in self.text]
            font_size = self.font.get_linesize()
            return (max(map(lambda x: x[0], sizes)),
                    len(sizes) * font_size + int((len(sizes)-1) * font_size * 0.4))
        else:
            return self.font.size(self.text)

    def bounds(self) -> pygame.Rect:
        bounds = pygame.Rect(0, 0, *self.size())
        if self.align & ALIGN_CENTER:
            bounds.centerx = WIN_WIDTH // 2 + self.x
        elif self.align & ALIGN_RIGHT:
            bounds.right = WIN_WIDTH - self.x
        else:
            bounds.left = self.x
        
        if self.align & VALIGN_CENTER:
            bounds.centery = WIN_HEIGHT // 2 + self.y
        elif self.align & VALIGN_BOTTOM:
            bounds.bottom = WIN_HEIGHT - self.y
        else:
            bounds.top = self.y
        return bounds


class Button(Text):
    def __init__(self,
                 text: str | list[str],
                 x: int,
                 y: int,
                 font: pygame.font.Font,
                 align: int = ALIGN_LEFT,
                 color: str | tuple[int, int, int] = 'white',
                 hover_color: str | tuple[int, int, int] = None,
                 func: Callable = None,
                 *func_args,
                 **func_kwargs):
        super().__init__(text, x, y, font, align, color, hover_color)
        self.func = func
        self.func_args = func_args
        self.func_kwargs = func_kwargs


class Input(Text):
    def __init__(self,
                 text: str | list[str],
                 x: int,
                 y: int,
                 font: pygame.font.Font,
                 align: int = ALIGN_LEFT,
                 color: str | tuple[int, int, int] = 'white',
                 hover_color: str | tuple[int, int, int] = None):
        super().__init__(text, x, y, font, align, color, hover_color)
        self._value = text
        self._cursor = ''

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, x):
        self._value = x
        self.text = self._value + self._cursor

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, x):
        self._cursor = x
        self.text = self._value + self._cursor


class Player:
    def __init__(self, name: str, job: str):
        self.name = name
        self.job = job


class Screen:
    def __init__(self, x = 0, y = 0, width = WIN_WIDTH, height = WIN_HEIGHT, elements = None):
        self.win = pygame.Surface((width, height))
        self.rect = self.win.get_rect(topleft=(x,y))
        self.elements = elements or []


class GameState:
    def __init__(self):
        self.screen = 'title'
        self.player_count = 1
        self.visible_elements = []
        self.current_player = 0
        self.players : list[Player] = []
        self.input_focused : Input = None


def main():

    # Initialize
    pygame.init()
    pygame.display.set_caption('Dungeons & Tickles Simulator')
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    game = GameState()
    
    # Fonts
    default_font = pygame.font.SysFont('Lucida Console', 15)
    medium_font = pygame.font.SysFont('Lucida Console', 25)
    title_font = pygame.font.SysFont('Lucida Console', 40)
    
    # Game elements
    game_elements = {
        'title': [
            Text('Dungeons & Tickles', 0, 20, title_font, ALIGN_CENTER),
            Text([
                'Welcome to the Dungeons & Tickles Simulator, made in Python 3.9 by JBtheShadow.',
                'As the name suggests, this is merely a simulator and not a full replacement of the original tabletop game.',
                'This is also a work in progress, subject to change.'
            ], 0, 100, default_font, ALIGN_CENTER),

            Text('What would you like to do?', 0, 250, default_font, ALIGN_CENTER),

            Button('Start a new game (overwrites current save)', 0, 320, medium_font, ALIGN_CENTER, 'cyan', 'red', change_screen, game, 'player_count'),
            Button('Load last saved game (if any)', 0, 370, medium_font, ALIGN_CENTER, 'cyan', 'red', change_screen, game, 'player_count'),
            Button('Quit to desktop', 0, 420, medium_font, ALIGN_CENTER, 'cyan', 'red', func=quit_to_desktop),
            (fps_text := Text('', 10, 10, default_font, VALIGN_BOTTOM)),
        ],
        'player_count': [
            Text('How many players will join this session?', 0, 300, medium_font, ALIGN_CENTER),

            Button('-', -30, 350, medium_font, ALIGN_CENTER, 'yellow', 'red', change_player_count, game, -1),
            (player_count_text := Text(f'{game.player_count}', 0, 350, medium_font, ALIGN_CENTER)),
            Button('+', +30, 350, medium_font, ALIGN_CENTER, 'yellow', 'red', change_player_count, game, 1),

            Button('Back', -50, 600, medium_font, ALIGN_CENTER, 'cyan', 'red', change_screen, game, 'title'),
            Button('Next', 50, 600, medium_font, ALIGN_CENTER, 'cyan', 'red', change_screen, game, 'player_setup'),
            fps_text,
        ],
        'player_setup': [
            (player_setup_text := Text('Player 1/1', 0, 50, medium_font, ALIGN_CENTER)),
            
            Text('Name:', -300, 150, medium_font, ALIGN_CENTER),
            (player_name_input := Input('Player 1', -300, 190, medium_font, ALIGN_CENTER)),

            Text('Job:', -300, 280, medium_font, ALIGN_CENTER),
            Button('<', -450, 320, medium_font, ALIGN_CENTER, 'yellow', 'red', change_player_job, game, -1),
            (player_job_name := Text('Warrior', -300, 320, medium_font, ALIGN_CENTER)),
            Button('>', -150, 320, medium_font, ALIGN_CENTER, 'yellow', 'red', change_player_job, game, 1),
            
            (player_job_description := Text('Warrior', 0, 400, default_font, ALIGN_CENTER)),

            Text('Stats:', 300, 150, medium_font, ALIGN_CENTER),
            (player_st_text := Text('ST: 100', 220, 200, medium_font, ALIGN_CENTER)),
            (player_mp_text := Text('MP: 50', 380, 200, medium_font, ALIGN_CENTER)),
            (player_at_text := Text('AT: 1', 220, 240, medium_font, ALIGN_CENTER)),
            (player_ep_text := Text('EP: 1', 380, 240, medium_font, ALIGN_CENTER)),
            (player_gold_text := Text('Gold: 50', 300, 280, medium_font, ALIGN_CENTER)),
            (player_faith_text := Text('Faith: 0', 300, 320, medium_font, ALIGN_CENTER)),

            Button('Back', -50, 600, medium_font, ALIGN_CENTER, 'cyan', 'red', setup_next_player, game, -1),
            Button('Next', 50, 600, medium_font, ALIGN_CENTER, 'cyan', 'red', setup_next_player, game, 1),
            fps_text,
        ],
    }

    cursor = '_'

    # Game loop
    while True:
        
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game.input_focused:
                    game.input_focused.cursor = CURSOR_NONE
                game.input_focused = None
                x, y = event.pos
                for element in visible_elements:
                    bounds = element.bounds() if isinstance(element, Text) else pygame.Rect()
                    if bounds.left <= x <= bounds.right and bounds.top <= y <= bounds.bottom:
                        if isinstance(element, Button) and element.func:
                            element.func(*element.func_args, **element.func_kwargs)
                            break
                        elif isinstance(element, Input):
                            game.input_focused = element
                            break

            if event.type == pygame.KEYDOWN:
                if game.input_focused is player_name_input:
                    keyboard_input(event, game.players[game.current_player], 'name')

        # Update state
        visible_elements = game_elements[game.screen]
        player = game.players[game.current_player] if len(game.players) else None
        job = JOBS[player.job] if player else None
        
        if player_count_text in visible_elements:
            player_count_text.text = f'{game.player_count}'

        if fps_text in visible_elements:
            fps_text.text = f'{int(clock.get_fps())} FPS'

        if player_setup_text in visible_elements:
            player_setup_text.text = f'Player {game.current_player + 1}/{game.player_count}'
        if player_name_input in visible_elements:
            player_name_input.value = player.name
        if player_job_name in visible_elements:
            player_job_name.text = JOBS[player.job].name
        if player_job_description in visible_elements:
            player_job_description.text = JOBS[player.job].description

        if player_st_text in visible_elements:
            player_st_text.text = f'ST: {job.st}'
        if player_mp_text in visible_elements:
            player_mp_text.text = f'MP: {job.mp}'
        if player_at_text in visible_elements:
            player_at_text.text = f'AT: {job.at}' if player.job != 'lee' else 'AT: -'
        if player_ep_text in visible_elements:
            player_ep_text.text = f'EP: {job.ep}'
        if player_gold_text in visible_elements:
            player_gold_text.text = f'Gold: {job.gold}'
        if player_faith_text in visible_elements:
            if not job.alignment:
                player_faith_text.text = 'Faith: 0'
            else:
                player_faith_text.text = f'Faith: {job.faith} ({"Good" if job.alignment == "good" else "Evil"})'

        if game.input_focused:
            input = game.input_focused
            new_cursor = CURSOR_FULL if pygame.time.get_ticks() % 1000 < 500 else CURSOR_EMPTY
            if new_cursor != input.cursor:
                input.cursor = new_cursor

        # Clear canvas
        win.fill('black')

        # Draw state
        for element in visible_elements:
            if isinstance(element, Text):
                draw_text(win, element)

        # Update pygame display
        pygame.display.update()

        # Limit FPS
        clock.tick(60)


if __name__ == '__main__':
    main()
