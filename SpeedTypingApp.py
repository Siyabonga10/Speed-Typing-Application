import pygame
from dataclasses import dataclass
from Menus import OptionsMenu
from itertools import chain
import sqlalchemy
from random import choice


@dataclass
class Pointer:
    row: int
    col: int


class SpeedTypingApp:

    def __init__(self, screen: pygame.surface.Surface):
        self.screen = screen
        self.height = screen.get_height()
        self.width = screen.get_width()
        self.font_size = 35
        self.text_renderer = pygame.font.Font("./assets/fonts/Exo-Bold.otf", self.font_size)

        self.engine = sqlalchemy.create_engine("sqlite+pysqlite:///database.db")
        self.passages_table = sqlalchemy.Table("passages", sqlalchemy.MetaData(), autoload_with=self.engine)

        self.passage = ""

        self.lines = []
        self.render_lines = []

        self.GREY = (80, 80, 80)
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)
        self.SCREEN_COLOR = (30, 30, 30)
        self.BLUE = (130, 130, 255)

        self.pointer = Pointer(0, 0)
        self.split_passage_to_lines()
        self.create_next_lines(self.pointer.row + 1)

        self.current_line = self.lines[self.pointer.row]
        self.current_line_data = []
        self.previous_lines_data = []
        pygame.key.start_text_input()

        self.create_current_line()
        self.start_y = 0.4*self.height
        self.target_y = self.start_y
        self.speed = 1
        self.offset_value = self.render_lines[0].get_height()

        self.notifications_banner = pygame.surface.Surface((self.width, 0.2*self.height), pygame.SRCALPHA)
        self.seconds = 60
        self.total_time = self.seconds*1000
        self.t1 = 0
        self.t2 = 0

        # Create the home menu
        self.menu_returns = [60, 180, 300]
        self.home_menu_options = ["1 MINUTE TEST", "3 MINUTE TEST", "5 MINUTE TEST"]
        self.home_menu = OptionsMenu(screen, self.home_menu_options, self.menu_returns, self.text_renderer, (0, 255, 255), (255, 255, 255))
        self.current_update = self.update_home_menu
        self.current_draw = self.draw_home_menu

        self.running = True
        self.game_clock = pygame.time.Clock()
        self.FPS = 60
        self.events = pygame.event.get()

        self.wpm = 0
        self.accuracy = 0
        self.end_of_game_screen = pygame.surface.Surface((0, 0))

        # Handle game sounds
        self.sound_channel = pygame.mixer.Channel(0)
        self.key_sound = pygame.mixer.Sound("./assets/sfx/sound.mp3")

    def split_passage_to_lines(self) -> None:
        self.choose_passage()
        avg_letters = self.width/(self.font_size*0.9)  # Some padding on the edges
        words = self.passage.split(" ")
        self.lines = []

        new_line = []
        current_letter_count = 0
        for word in words:
            current_letter_count += len(word)
            new_line.append(word)

            if current_letter_count > avg_letters:
                current_letter_count = 0
                self.lines.append(" ".join(new_line).strip())
                new_line = []

        self.render_lines = [None] * len(self.lines)

    def create_next_lines(self, first_index: int) -> None:
        for i in range(first_index, len(self.lines)):
            row = self.lines[i]
            line = self.text_renderer.render(row, True, self.GREY)
            self.render_lines[i] = line

    def render_next_lines(self) -> None:
        offset = self.font_size * 1.1
        y_coord = self.start_y

        for line in self.render_lines:
            if line:
                position_rect = line.get_rect()
                position_rect.centerx = self.width/2
                position_rect.centery = y_coord
                y_coord += offset
                self.screen.blit(line, position_rect)

        self.screen.blit(self.notifications_banner, (0, 0))

    def event_handler(self):
        self.t2 = pygame.time.get_ticks()
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                self.sound_channel.play(self.key_sound)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE and self.pointer.col > 0:
                self.pointer.col -= 1
                del self.current_line_data[self.pointer.col]
                self.create_current_line()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE and self.pointer.row > 0:
                self.current_line_data = self.previous_lines_data[self.pointer.row - 1].copy()
                del self.previous_lines_data[self.pointer.row - 1]
                self.pointer.row -= 1
                self.pointer.col = len(self.lines[self.pointer.row]) - 1
                self.create_current_line()
                self.create_next_lines(self.pointer.row+1)
                self.target_y += self.offset_value
                self.speed = +1
            elif event.type == pygame.TEXTINPUT:
                if self.pointer.col == len(self.lines[self.pointer.row]):
                    self.pointer.row += 1
                    self.pointer.col = 0
                    self.previous_lines_data.append(self.current_line_data.copy())
                    self.current_line_data = []
                    self.target_y -= self.offset_value
                    self.speed = -1

                else:
                    letter = event.text
                    if letter == self.lines[self.pointer.row][self.pointer.col]:
                        self.current_line_data.append(True)
                    else:
                        self.current_line_data.append(False)
                    self.pointer.col += 1
                    self.create_current_line()
            elif self.pointer.row == len(self.lines) - 1 and self.pointer.col == len(self.lines[self.pointer.row]):
                self.previous_lines_data.append(self.current_line_data)
                self.compute_player_wpm()
                self.create_end_of_test_screen()
                self.current_update = self.update_end_of_game
                self.current_draw = self.draw_end_of_game
                self.pointer = Pointer(0, 0)
        self.transition()
        self.update_time_banner()

        # Check for the timeout
        if self.t2 - self.t1 >= self.total_time:
            self.previous_lines_data.append(self.current_line_data)
            self.compute_player_wpm()
            self.create_end_of_test_screen()
            self.current_update = self.update_end_of_game
            self.current_draw = self.draw_end_of_game
            self.reset()

    def resize(self):
        self.height = self.screen.get_height()
        self.width = self.screen.get_width()
        self.split_passage_to_lines()
        self.create_next_lines(0)

    def create_current_line(self):
        # Create a background for the rendering
        line = self.text_renderer.render(self.lines[self.pointer.row] + " "*3, True, self.GREY)
        line.fill((0, 0, 0))
        line.set_colorkey((0, 0, 0))
        sentence = self.lines[self.pointer.row]
        left = 0
        for i in range(self.pointer.col):
            letter = sentence[i]
            color = self.WHITE if self.current_line_data[i] else self.RED
            letter = self.text_renderer.render(letter, True, color)
            letter_pos = letter.get_rect()
            letter_pos.left = left
            left += letter.get_width()
            line.blit(letter, letter_pos)
        for i in range(self.pointer.col, len(sentence)):
            letter = sentence[i]
            letter = self.text_renderer.render(letter, True, self.GREY)
            letter_pos = letter.get_rect()
            letter_pos.left = left
            left += letter.get_width()
            line.blit(letter, letter_pos)

        self.render_lines[self.pointer.row] = line

    def transition(self):
        if self.start_y != self.target_y:
            self.start_y += self.speed

    def update_time_banner(self):
        time_left = self.total_time - (self.t2 - self.t1)
        time_bar = pygame.surface.Surface((0.8*self.width, 0.03*self.height), pygame.SRCALPHA)
        bg_rect = time_bar.get_rect()
        pygame.draw.rect(time_bar, self.BLUE, bg_rect, width=2, border_radius=2)
        bg_rect.right = bg_rect.width * (time_left / self.total_time)
        pygame.draw.rect(time_bar, self.BLUE, bg_rect, border_radius=2)

        rect = time_bar.get_rect()
        self.notifications_banner.fill(self.SCREEN_COLOR)
        rect.center = self.notifications_banner.get_rect().center

        self.notifications_banner.blit(time_bar, rect)

    def update_home_menu(self):
        time = self.home_menu.event_handler(self.events)
        if time:
            self.seconds = time
            self.total_time = self.seconds*1000
            self.current_update = self.event_handler
            self.current_draw = self.render_next_lines

            self.t2 = pygame.time.get_ticks()
            self.t1 = pygame.time.get_ticks()

    def draw_home_menu(self):
        self.home_menu.draw()

    def show_home_menu(self):
        self.current_update = self.update_home_menu
        self.current_draw = self.draw_home_menu

    def main_update(self):
        self.current_update()

    def draw_main(self):
        self.current_draw()

    def run_game(self):
        while self.running:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(self.SCREEN_COLOR)
            self.main_update()
            self.draw_main()
            pygame.display.flip()
            self.game_clock.tick(self.FPS)

    def create_end_of_test_screen(self):
        self.end_of_game_screen = pygame.surface.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.end_of_game_screen.fill(self.SCREEN_COLOR)

        wpm_msg = self.text_renderer.render(f"Your WPM: {self.wpm}", True, self.WHITE)
        pos = wpm_msg.get_rect()
        pos.center = self.screen.get_rect().center
        self.end_of_game_screen.blit(wpm_msg, pos)

        acc_msg = self.text_renderer.render(f"Accuracy: {self.accuracy}", True, self.WHITE)
        pos = acc_msg.get_rect()
        pos.centerx = self.screen.get_rect().centerx
        pos.centery = self.screen.get_rect().centery*0.55
        self.end_of_game_screen.blit(acc_msg, pos)

        return_msg = self.text_renderer.render("Press enter to return to the main menu", True, self.WHITE)
        pos = return_msg.get_rect()
        pos.centerx = self.screen.get_rect().centerx
        pos.centery = self.screen.get_height()*0.9
        self.end_of_game_screen.blit(return_msg, pos)

    def update_end_of_game(self):
        for event in self.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.show_home_menu()
                self.reset()

    def draw_end_of_game(self):
        self.screen.blit(self.end_of_game_screen, (0, 0))

    def compute_player_wpm(self):
        time_taken = (self.t2 - self.t1)/(1000*60)      # Conversion to minutes

        words = 0
        for i in range(self.pointer.row + 1):
            line_len = len(self.lines[i]) if i != self.pointer.row else self.pointer.col
            for j in range(line_len):
                if self.lines[i][j] == ' ':
                    words += 1
            words += 1

        self.wpm = round(words/time_taken)

        typing_data = list(chain.from_iterable(self.previous_lines_data))
        correct_count = len(list(filter(lambda bool_val: bool_val, typing_data)))
        if len(typing_data) == 0:
            self.accuracy = 0
            return
        self.accuracy = round((correct_count*100)/len(typing_data), 2)

    def reset(self):
        self.current_line = self.lines[self.pointer.row]
        self.current_line_data = []
        self.previous_lines_data = []
        self.pointer = Pointer(0, 0)
        self.split_passage_to_lines()
        self.create_next_lines(self.pointer.row)
        self.start_y = 0.4 * self.height
        self.target_y = self.start_y

    def choose_passage(self):
        choices = []
        cmd = sqlalchemy.select(self.passages_table)
        cmd.compile()

        with self.engine.connect() as conn:
            for row in conn.execute(cmd):

                choices.append(row[0])

        self.passage = choice(choices)

