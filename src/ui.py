from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Protocol

import pygame

WIN_WIDTH = 1280
WIN_HEIGHT = 720

WHITE = "white"
CYAN = "cyan"
YELLOW = "yellow"
RED = "red"

CURSOR_NONE = ""
CURSOR_EMPTY = " "
CURSOR_FULL = "■"


class Align(Enum):
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()


class VAlign(Enum):
    TOP = auto()
    MIDDLE = auto()
    BOTTOM = auto()


class TextElement(Protocol):
    text: str
    color: str
    hover_color: str
    font: pygame.font.Font
    align: Align

    def bounds(self) -> pygame.Rect:
        ...


@dataclass
class Text:
    x: int
    y: int
    text: str
    font: pygame.font.Font
    align: Align = Align.LEFT
    v_align: VAlign = VAlign.TOP
    color: str = WHITE
    hover_color: str = None

    def size(self):
        lines = self.text.split("\n")
        sizes = [self.font.size(text) for text in lines]
        font_size = self.font.get_linesize()
        width = max(map(lambda x: x[0], sizes))
        height = len(sizes) * font_size + 0.4 * int((len(sizes) - 1) * font_size)
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

    def click(self):
        pass


def nop():
    pass


@dataclass
class Button:
    text: Text
    func: Callable = None
    func_args: list = None
    func_kwargs: dict = None

    def __post_init__(self):
        self.func = self.func or nop
        self.func_args = self.func_args or []
        self.func_kwargs = self.func_kwargs or {}

    def click(self) -> None:
        self.func(*self.func_args, **self.func_kwargs)

    def bounds(self):
        return self.text.bounds()

    def draw(self, win):
        self.text.draw(win)


@dataclass
class Input:
    text: Text
    focus: Callable[[Input], None] = None
    _value: str = field(init=False)
    _cursor: str = field(init=False)

    def __post_init__(self):
        self._value = self.text.text
        self._cursor = CURSOR_NONE

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, x):
        self._value = x
        self.text.text = self._value + self._cursor

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, x):
        self._cursor = x
        self.text.text = self._value + self._cursor

    def click(self) -> None:
        self.focus(self)

    def bounds(self):
        return self.text.bounds()

    def draw(self, win):
        draw_text(win, self.text)


def draw_text(win: pygame.Surface, element: TextElement):
    bounds = element.bounds()

    color = element.color
    if element.hover_color:
        x, y = pygame.mouse.get_pos()
        if bounds.left <= x <= bounds.right and bounds.top <= y <= bounds.bottom:
            color = element.hover_color

    rows = element.text.split("\n")
    text_surf = pygame.Surface((bounds.width, bounds.height))
    offset_y = 0
    step_y = int(element.font.get_linesize() * 1.4)
    for row in rows:
        text = element.font.render(row, True, color)
        rect = text.get_rect()
        if element.align == Align.CENTER:
            rect.centerx = bounds.width // 2
        elif element.align == Align.RIGHT:
            rect.right = bounds.width
        rect.top = offset_y
        offset_y += step_y
        text_surf.blit(text, rect)
    win.blit(text_surf, bounds)
