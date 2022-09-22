from __future__ import annotations
from abc import ABC
from typing import Callable
from dataclasses import dataclass, field
from enum import Enum, auto
import sys
import pygame

from job import JOBS, JobID


WIN_WIDTH = 1280
WIN_HEIGHT = 720

WHITE = 'white'
CYAN = 'cyan'
YELLOW = 'yellow'
RED = 'red'

CURSOR_NONE = ''
CURSOR_EMPTY = ' '
CURSOR_FULL = '■'


def nop():
    pass


def quit_to_desktop():
    pygame.event.post(pygame.event.Event(pygame.QUIT, {}))


def set_focus(game: GameState, element: Input):
    game.input_focused = element


def draw_text(win: pygame.Surface, text: Text):
    bounds = text.bounds()

    color = text.color
    if text.hover_color:
        x, y = pygame.mouse.get_pos()
        if (bounds.left <= x <= bounds.right
                and bounds.top <= y <= bounds.bottom):
            color = text.hover_color

    lines = text.text.split('\n')
    text_surf = pygame.Surface((bounds.width, bounds.height))
    offset_y = 0
    step_y = int(text.font.get_linesize() * 1.4)
    for item in lines:
        t_surf = text.font.render(item, True, color)
        t_rect = t_surf.get_rect()
        if text.align == Align.CENTER:
            t_rect.centerx = bounds.width // 2
        elif text.align == Align.RIGHT:
            t_rect.right = bounds.width
        t_rect.top = offset_y
        offset_y += step_y
        text_surf.blit(t_surf, t_rect)

    win.blit(text_surf, bounds)


def change_player_count(state: GameState, value):
    state.player_count += value
    state.player_count = max(1, min(state.player_count, 6))


def change_player_job(state: GameState, value):
    player = state.players[state.current_player]
    i = list(JOBS).index(player.job_id) + value
    if i < 0:
        i = len(JOBS) - 1
    elif i >= len(JOBS):
        i = 0
    player.job_id = list(JOBS)[i]


def change_screen(state: GameState, screen):
    if screen == ScreenID.PLAYER_COUNT:
        if state.screen == ScreenID.TITLE:
            state.player_count = 1
    if screen == ScreenID.PLAYER_SETUP:
        if state.screen == ScreenID.PLAYER_COUNT:
            state.current_player = 0
            state.players = [Player(f'Player {i}')
                             for i in range(1, state.player_count + 1)]
    state.screen = screen


def setup_next_player(state: GameState, next):
    state.current_player += next
    if state.current_player < 0:
        state.current_player = 0
        change_screen(state, ScreenID.PLAYER_COUNT)
        return
    elif state.current_player >= state.player_count:
        state.current_player = state.player_count - 1
        change_screen(state, ScreenID.SETUP_CONFIRM)
        return


def keyboard_input(event, obj, field):
    if event.key == pygame.K_BACKSPACE:
        setattr(obj, field, getattr(obj, field)[:-1])
    elif event.key not in [pygame.K_RETURN, pygame.K_TAB] and event.unicode:
        setattr(obj, field, getattr(obj, field) + event.unicode)


@dataclass
class UIElement(ABC):
    x: int
    y: int

    def size(self) -> tuple[int, int]:
        pass

    def bounds(self) -> pygame.Rect:
        pass

    def draw(self, win: pygame.Surface) -> None:
        pass

    def click(self) -> None:
        pass


class Align(Enum):
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()


class VAlign(Enum):
    TOP = auto()
    MIDDLE = auto()
    BOTTOM = auto()


@dataclass
class Text(UIElement):
    text: str
    font: pygame.font.Font
    align: Align = Align.LEFT
    v_align: VAlign = VAlign.TOP
    color: str = WHITE
    hover_color: str = None

    def size(self):
        lines = self.text.split('\n')
        sizes = [self.font.size(text) for text in lines]
        font_size = self.font.get_linesize()
        width = max(map(lambda x: x[0], sizes))
        height = (len(sizes) * font_size
                  + 0.4 * int((len(sizes)-1) * font_size))
        return width, height

    def bounds(self):
        bounds = pygame.Rect(0, 0, *self.size())
        if self.align == Align.CENTER:
            bounds.centerx = WIN_WIDTH // 2 + self.x
        elif self.align == Align.RIGHT:
            bounds.right = WIN_WIDTH - self.x
        else:
            bounds.left = self.x
        if self.v_align == VAlign.MIDDLE:
            bounds.centery = WIN_HEIGHT // 2 + self.y
        elif self.v_align == VAlign.BOTTOM:
            bounds.bottom = WIN_HEIGHT - self.y
        else:
            bounds.top = self.y
        return bounds

    def draw(self, win):
        draw_text(win, self)


@dataclass
class Button(Text):
    func: Callable = None
    func_args: list = None
    func_kwargs: dict = None

    def __post_init__(self):
        self.func = self.func or nop
        self.func_args = self.func_args or []
        self.func_kwargs = self.func_kwargs or {}

    def click(self) -> None:
        self.func(*self.func_args, **self.func_kwargs)


@dataclass
class Input(Text):
    focus: Callable[[GameState, Input], None] = None
    game: GameState = None
    _value: str = field(init=False)
    _cursor: str = field(init=False)

    def __post_init__(self):
        self._value = self.text
        self._cursor = CURSOR_NONE

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

    def click(self) -> None:
        self.focus(self.game, self)


@dataclass
class Player:
    name: str
    race: str = 'Human'
    job_id: JobID = JobID.WARRIOR


class Screen:
    def __init__(self, x=0, y=0, width=WIN_WIDTH, height=WIN_HEIGHT,
                 elements=None):
        self.win = pygame.Surface((width, height))
        self.rect = self.win.get_rect(topleft=(x, y))
        self.elements = elements or []


class GameState:
    def __init__(self):
        self.screen = ScreenID.TITLE
        self.player_count = 1
        self.visible_elements = []
        self.current_player = 0
        self.players: list[Player] = []
        self.input_focused: Input = None


class ScreenID(Enum):
    TITLE = auto()
    PLAYER_COUNT = auto()
    PLAYER_SETUP = auto()
    SETUP_CONFIRM = auto()


def main():

    # Initialize
    pygame.init()
    pygame.display.set_caption('Dungeons & Tickles Simulator')
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    game = GameState()

    # Fonts
    default_font = pygame.font.SysFont('Lucida Console', 15)
    option_font = pygame.font.SysFont('Lucida Console', 20)
    medium_font = pygame.font.SysFont('Lucida Console', 25)
    title_font = pygame.font.SysFont('Lucida Console', 40)

    # Game elements
    visible_elements: list[UIElement] = []
    screens: dict[ScreenID, list[UIElement]] = {
        ScreenID.TITLE: [
            Text(0, 20, 'Dungeons & Tickles', title_font, Align.CENTER),
            Text(
                0, 100,
                'Welcome to the Dungeons & Tickles Simulator, made in Python '
                '3.9 by JBtheShadow.\n'
                'As the name suggests, this is merely a simulator and not a '
                'full replacement of the original tabletop game.\n'
                'This is also a work in progress, subject to change.',
                default_font, Align.CENTER),

            Text(0, 250, 'What would you like to do?',
                 default_font, Align.CENTER),

            Button(0, 320, 'Start a new game (overwrites current save)',
                   medium_font, Align.CENTER, VAlign.TOP, CYAN, RED,
                   change_screen, [game, ScreenID.PLAYER_COUNT]),
            Button(0, 370, 'Load last saved game (if any)', medium_font,
                   Align.CENTER, VAlign.TOP, CYAN, RED,
                   change_screen, [game, ScreenID.PLAYER_COUNT]),
            Button(4, 420, 'Quit to desktop',
                   medium_font, Align.CENTER, VAlign.TOP, CYAN, RED,
                   quit_to_desktop),
            (fps_text := Text(10, 10, '',
                              default_font, v_align=VAlign.BOTTOM)),
        ],
        ScreenID.PLAYER_COUNT: [
            Text(0, 300, 'How many players will join this session?',
                 medium_font, Align.CENTER),

            Button(-30, 350, '-', option_font, Align.CENTER, VAlign.TOP,
                   YELLOW, RED, change_player_count, [game, -1]),
            (player_count_text := Text(0, 350, f'{game.player_count}',
                                       option_font, Align.CENTER)),
            Button(30, 350, '+', option_font, Align.CENTER, VAlign.TOP,
                   YELLOW, RED, change_player_count, [game, 1]),

            Button(-50, 600, 'Back', medium_font, Align.CENTER, VAlign.TOP,
                   CYAN, RED, change_screen, [game, ScreenID.TITLE]),
            Button(50, 600, 'Next', medium_font, Align.CENTER, VAlign.TOP,
                   CYAN, RED,
                   change_screen, [game, ScreenID.PLAYER_SETUP]),
            fps_text,
        ],
        ScreenID.PLAYER_SETUP: [
            (player_setup_text := Text(0, 50, 'Player 1 of 1',
                                       medium_font, Align.CENTER)),

            Text(-300, 150, 'Name:', medium_font, Align.CENTER),
            (player_name_input := Input(
                -300, 180, 'Player 1', option_font, Align.CENTER,
                focus=set_focus, game=game)),

            Text(-300, 215, 'Race:', medium_font, Align.CENTER),
            (player_race_input := Input(
                -300, 245, 'Human', option_font, Align.CENTER,
                focus=set_focus, game=game)),

            Text(-300, 280, 'Job:', medium_font, Align.CENTER),
            Button(-410, 310, '<', option_font,
                   Align.CENTER, VAlign.TOP, YELLOW, RED,
                   change_player_job, [game, -1]),
            (player_job_name := Text(-300, 310, JOBS[JobID.WARRIOR].name,
                                     option_font, Align.CENTER)),
            Button(-190, 310, '>', option_font,
                   Align.CENTER, VAlign.TOP, YELLOW, RED,
                   change_player_job, [game, 1]),

            (player_job_description := Text(
                0, 400, JOBS[JobID.WARRIOR].description,
                default_font, Align.CENTER)),

            Text(300, 150, 'Stats:', medium_font, Align.CENTER),
            (player_st_text := Text(250, 200, 'ST: 100',
                                    option_font, Align.CENTER)),
            (player_mp_text := Text(350, 200, 'MP: 50',
                                    option_font, Align.CENTER)),
            (player_at_text := Text(250, 240, 'AT: 1',
                                    option_font, Align.CENTER)),
            (player_ep_text := Text(350, 240, 'EP: 1',
                                    option_font, Align.CENTER)),
            (player_gold_text := Text(300, 280, 'Gold: 50',
                                      option_font, Align.CENTER)),
            (player_faith_text := Text(300, 320, 'Faith: 0',
                                       option_font, Align.CENTER)),

            Button(-50, 600, 'Back', medium_font,
                   Align.CENTER, VAlign.TOP, CYAN, RED,
                   setup_next_player, [game, -1]),
            Button(50, 600, 'Next', medium_font,
                   Align.CENTER, VAlign.TOP, CYAN, RED,
                   setup_next_player, [game, 1]),
            fps_text,
        ],
        ScreenID.SETUP_CONFIRM: [
            Text(0, 50, 'Start a game with these players?',
                 medium_font, Align.CENTER),

            (setup_confirm_text := Text(0, 200, '',
                                        option_font, Align.CENTER)),

            Button(-50, 600, 'Back', medium_font,
                   Align.CENTER, VAlign.TOP, CYAN, RED,
                   change_screen, [game, ScreenID.PLAYER_SETUP]),
            Button(50, 600, 'CONFIRM', medium_font,
                   Align.CENTER, VAlign.TOP, CYAN, RED,
                   change_screen, [game, ScreenID.SETUP_CONFIRM]),
            fps_text,
        ],
    }

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
                    bounds = element.bounds()
                    if (bounds.left <= x <= bounds.right
                            and bounds.top <= y <= bounds.bottom):
                        element.click()
                        break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and game.input_focused:
                    game.input_focused.cursor = CURSOR_NONE
                    game.input_focused = None

                if game.input_focused:
                    if game.input_focused is player_name_input:
                        obj, field = game.players[game.current_player], 'name'
                    if game.input_focused is player_race_input:
                        obj, field = game.players[game.current_player], 'race'

                    if obj and field:
                        keyboard_input(event, obj, field)

        # Update state
        visible_elements = screens[game.screen]
        player = (game.players[game.current_player] if len(game.players)
                  else None)
        job = JOBS[player.job_id] if player else None

        if player_count_text in visible_elements:
            player_count_text.text = f'{game.player_count}'

        if fps_text in visible_elements:
            fps_text.text = f'{int(clock.get_fps())} FPS'

        if player_setup_text in visible_elements:
            player_setup_text.text = (f'Player {game.current_player + 1} of '
                                      f'{game.player_count}')
        if player_name_input in visible_elements:
            player_name_input.value = player.name
        if player_race_input in visible_elements:
            player_race_input.value = player.race
        if player_job_name in visible_elements:
            player_job_name.text = JOBS[player.job_id].name
        if player_job_description in visible_elements:
            player_job_description.text = JOBS[player.job_id].description

        if player_st_text in visible_elements:
            player_st_text.text = f'ST: {job.st}'
        if player_mp_text in visible_elements:
            player_mp_text.text = f'MP: {job.mp}'
        if player_at_text in visible_elements:
            player_at_text.text = (
                f'AT: {job.at}' if player.job_id != JobID.LEE
                else 'AT: -'
            )
        if player_ep_text in visible_elements:
            player_ep_text.text = f'EP: {job.ep}'
        if player_gold_text in visible_elements:
            player_gold_text.text = f'Gold: {job.gold}'
        if player_faith_text in visible_elements:
            if not job.alignment:
                player_faith_text.text = 'Faith: 0'
            else:
                player_faith_text.text = (
                    f'Faith: {job.faith} ('
                    f'{"Good" if job.alignment == "good" else "Evil"})'
                )

        if setup_confirm_text in visible_elements:
            setup_confirm_text.text = '\n'.join([
                f'{p.name} the {p.race} {JOBS[p.job_id].name}'
                for p in game.players
            ])

        if game.input_focused:
            input = game.input_focused
            new_cursor = (
                CURSOR_FULL if pygame.time.get_ticks() % 1000 < 500
                else CURSOR_EMPTY
            )
            if new_cursor != input.cursor:
                input.cursor = new_cursor

        # Clear canvas
        win.fill('black')

        # Draw state
        for element in visible_elements:
            element.draw(win)

        # Update pygame display
        pygame.display.update()

        # Limit FPS
        clock.tick(60)


if __name__ == '__main__':
    main()
