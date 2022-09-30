from __future__ import annotations

import sys
from dataclasses import dataclass
from enum import Enum, auto
from functools import partial
from typing import Protocol

import pygame

from job import JOBS, JobID
from ui import (
    CURSOR_EMPTY,
    CURSOR_FULL,
    CURSOR_NONE,
    CYAN,
    RED,
    WIN_HEIGHT,
    WIN_WIDTH,
    YELLOW,
    Align,
    Button,
    Input,
    Text,
    VAlign,
)


def quit_to_desktop():
    pygame.event.post(pygame.event.Event(pygame.QUIT, {}))


def set_focus(game: GameState, element: Input):
    game.input_focused = element


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
            state.players = [
                Player(f"Player {i}") for i in range(1, state.player_count + 1)
            ]
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


class UIElement(Protocol):
    def draw(self) -> None:
        ...

    def bounds(self) -> pygame.Rect:
        ...

    def click(self) -> None:
        ...


@dataclass
class Player:
    name: str
    race: str = "Human"
    job_id: JobID = JobID.WARRIOR


# class Screen:
#     def __init__(self, x=0, y=0, width=WIN_WIDTH, height=WIN_HEIGHT, elements=None):
#         self.win = pygame.Surface((width, height))
#         self.rect = self.win.get_rect(topleft=(x, y))
#         self.elements = elements or []


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
    pygame.display.set_caption("Dungeons & Tickles Simulator")
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    game = GameState()
    on_focus = partial(set_focus, game)

    # Fonts
    default_font = pygame.font.SysFont("Lucida Console", 15)
    option_font = pygame.font.SysFont("Lucida Console", 20)
    medium_font = pygame.font.SysFont("Lucida Console", 25)
    title_font = pygame.font.SysFont("Lucida Console", 40)

    # Game elements
    visible_elements: list[UIElement] = []
    screens: dict[ScreenID, list[UIElement]] = {
        ScreenID.TITLE: [
            Text(0, 20, "Dungeons & Tickles", title_font, Align.CENTER),
            Text(
                0,
                100,
                "Welcome to the Dungeons & Tickles Simulator, made in Python "
                "3.9 by JBtheShadow.\n"
                "As the name suggests, this is merely a simulator and not a "
                "full replacement of the original tabletop game.\n"
                "This is also a work in progress, subject to change.",
                default_font,
                Align.CENTER,
            ),
            Text(0, 250, "What would you like to do?", default_font, Align.CENTER),
            Button(
                Text(
                    0,
                    320,
                    "Start a new game (overwrites current save)",
                    medium_font,
                    Align.CENTER,
                    VAlign.TOP,
                    CYAN,
                    RED,
                ),
                change_screen,
                [game, ScreenID.PLAYER_COUNT],
            ),
            Button(
                Text(
                    0,
                    370,
                    "Load last saved game (if any)",
                    medium_font,
                    Align.CENTER,
                    VAlign.TOP,
                    CYAN,
                    RED,
                ),
                change_screen,
                [game, ScreenID.PLAYER_COUNT],
            ),
            Button(
                Text(
                    4,
                    420,
                    "Quit to desktop",
                    medium_font,
                    Align.CENTER,
                    VAlign.TOP,
                    CYAN,
                    RED,
                ),
                quit_to_desktop,
            ),
            (fps_text := Text(10, 10, "", default_font, v_align=VAlign.BOTTOM)),
        ],
        ScreenID.PLAYER_COUNT: [
            Text(
                0,
                300,
                "How many players will join this session?",
                medium_font,
                Align.CENTER,
            ),
            Button(
                Text(-30, 350, "-", option_font, Align.CENTER, VAlign.TOP, YELLOW, RED),
                change_player_count,
                [game, -1],
            ),
            (
                player_count_text := Text(
                    0, 350, f"{game.player_count}", option_font, Align.CENTER
                )
            ),
            Button(
                Text(30, 350, "+", option_font, Align.CENTER, VAlign.TOP, YELLOW, RED),
                change_player_count,
                [game, 1],
            ),
            Button(
                Text(
                    -50, 600, "Back", medium_font, Align.CENTER, VAlign.TOP, CYAN, RED
                ),
                change_screen,
                [game, ScreenID.TITLE],
            ),
            Button(
                Text(50, 600, "Next", medium_font, Align.CENTER, VAlign.TOP, CYAN, RED),
                change_screen,
                [game, ScreenID.PLAYER_SETUP],
            ),
            fps_text,
        ],
        ScreenID.PLAYER_SETUP: [
            (
                player_setup_text := Text(
                    0, 50, "Player 1 of 1", medium_font, Align.CENTER
                )
            ),
            Text(-300, 150, "Name:", medium_font, Align.CENTER),
            (
                player_name_input := Input(
                    Text(-300, 180, "Player 1", option_font, Align.CENTER),
                    focus=on_focus,
                )
            ),
            Text(-300, 215, "Race:", medium_font, Align.CENTER),
            (
                player_race_input := Input(
                    Text(-300, 245, "Human", option_font, Align.CENTER),
                    focus=on_focus,
                )
            ),
            Text(-300, 280, "Job:", medium_font, Align.CENTER),
            Button(
                Text(
                    -410, 310, "<", option_font, Align.CENTER, VAlign.TOP, YELLOW, RED
                ),
                change_player_job,
                [game, -1],
            ),
            (
                player_job_name := Text(
                    -300, 310, JOBS[JobID.WARRIOR].name, option_font, Align.CENTER
                )
            ),
            Button(
                Text(
                    -190, 310, ">", option_font, Align.CENTER, VAlign.TOP, YELLOW, RED
                ),
                change_player_job,
                [game, 1],
            ),
            (
                player_job_description := Text(
                    0, 400, JOBS[JobID.WARRIOR].description, default_font, Align.CENTER
                )
            ),
            Text(300, 150, "Stats:", medium_font, Align.CENTER),
            (player_st_text := Text(250, 200, "ST: 100", option_font, Align.CENTER)),
            (player_mp_text := Text(350, 200, "MP: 50", option_font, Align.CENTER)),
            (player_at_text := Text(250, 240, "AT: 1", option_font, Align.CENTER)),
            (player_ep_text := Text(350, 240, "EP: 1", option_font, Align.CENTER)),
            (player_gold_text := Text(300, 280, "Gold: 50", option_font, Align.CENTER)),
            (
                player_faith_text := Text(
                    300, 320, "Faith: 0", option_font, Align.CENTER
                )
            ),
            Button(
                Text(
                    -50, 600, "Back", medium_font, Align.CENTER, VAlign.TOP, CYAN, RED
                ),
                setup_next_player,
                [game, -1],
            ),
            Button(
                Text(50, 600, "Next", medium_font, Align.CENTER, VAlign.TOP, CYAN, RED),
                setup_next_player,
                [game, 1],
            ),
            fps_text,
        ],
        ScreenID.SETUP_CONFIRM: [
            Text(0, 50, "Start a game with these players?", medium_font, Align.CENTER),
            (setup_confirm_text := Text(0, 200, "", option_font, Align.CENTER)),
            Button(
                Text(
                    -50, 600, "Back", medium_font, Align.CENTER, VAlign.TOP, CYAN, RED
                ),
                change_screen,
                [game, ScreenID.PLAYER_SETUP],
            ),
            Button(
                Text(
                    50, 600, "CONFIRM", medium_font, Align.CENTER, VAlign.TOP, CYAN, RED
                ),
                change_screen,
                [game, ScreenID.SETUP_CONFIRM],
            ),
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
                    if (
                        bounds.left <= x <= bounds.right
                        and bounds.top <= y <= bounds.bottom
                    ):
                        element.click()
                        break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and game.input_focused:
                    game.input_focused.cursor = CURSOR_NONE
                    game.input_focused = None

                if game.input_focused:
                    if game.input_focused is player_name_input:
                        obj, field = game.players[game.current_player], "name"
                    if game.input_focused is player_race_input:
                        obj, field = game.players[game.current_player], "race"

                    if obj and field:
                        keyboard_input(event, obj, field)

        # Update state
        visible_elements = screens[game.screen]
        player = game.players[game.current_player] if len(game.players) else None
        job = JOBS[player.job_id] if player else None

        if player_count_text in visible_elements:
            player_count_text.text = f"{game.player_count}"

        if fps_text in visible_elements:
            fps_text.text = f"{int(clock.get_fps())} FPS"

        if player_setup_text in visible_elements:
            player_setup_text.text = (
                f"Player {game.current_player + 1} of " f"{game.player_count}"
            )
        if player_name_input in visible_elements:
            player_name_input.value = player.name
        if player_race_input in visible_elements:
            player_race_input.value = player.race
        if player_job_name in visible_elements:
            player_job_name.text = JOBS[player.job_id].name
        if player_job_description in visible_elements:
            player_job_description.text = JOBS[player.job_id].description

        if player_st_text in visible_elements:
            player_st_text.text = f"ST: {job.st}"
        if player_mp_text in visible_elements:
            player_mp_text.text = f"MP: {job.mp}"
        if player_at_text in visible_elements:
            player_at_text.text = (
                f"AT: {job.at}" if player.job_id != JobID.LEE else "AT: -"
            )
        if player_ep_text in visible_elements:
            player_ep_text.text = f"EP: {job.ep}"
        if player_gold_text in visible_elements:
            player_gold_text.text = f"Gold: {job.gold}"
        if player_faith_text in visible_elements:
            if not job.alignment:
                player_faith_text.text = "Faith: 0"
            else:
                player_faith_text.text = (
                    f"Faith: {job.faith} ("
                    f'{"Good" if job.alignment == "good" else "Evil"})'
                )

        if setup_confirm_text in visible_elements:
            setup_confirm_text.text = "\n".join(
                [f"{p.name} the {p.race} {JOBS[p.job_id].name}" for p in game.players]
            )

        if game.input_focused:
            input = game.input_focused
            new_cursor = (
                CURSOR_FULL if pygame.time.get_ticks() % 1000 < 500 else CURSOR_EMPTY
            )
            if new_cursor != input.cursor:
                input.cursor = new_cursor

        # Clear canvas
        win.fill("black")

        # Draw state
        for element in visible_elements:
            element.draw(win)

        # Update pygame display
        pygame.display.update()

        # Limit FPS
        clock.tick(60)


if __name__ == "__main__":
    main()
