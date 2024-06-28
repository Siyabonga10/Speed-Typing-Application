import pygame

# Used for the main menu, takes in a set of options to display to the user
# and items to return in the event that the user selects on of the options
# these can be numbers, callback function etc.
class OptionsMenu:
    def __init__(self, screen: pygame.surface.Surface, options: list[str], callbacks: list[any], font_renderer: pygame.font.Font, color: tuple[int, int, int], select_color: tuple[int, int, int]):
        self.screen = screen
        self.options = options.copy()
        self.return_options = callbacks

        if len(self.options) != len(self.return_options):
            print("ERROR: Menu object instantiation failed.")
            return

        self.font_renderer = font_renderer
        self.font_size = font_renderer.get_height()
        self.spacing = 1.3*self.font_size

        self.start_y = self.screen.get_rect().centery - (self.spacing*len(self.options))/2
        self.center_x = self.screen.get_rect().centerx

        self.current_selection_index = 0
        self.color = color
        self.selection_color = select_color

        self.active = True

    def draw(self):
        y_coord = self.start_y
        for option in self.options:
            color = self.color if self.options[self.current_selection_index] == option else self.selection_color
            option = self.font_renderer.render(option, True, color)
            position = option.get_rect()
            position.centerx = self.center_x
            position.centery = y_coord
            y_coord += self.spacing
            self.screen.blit(option, position)

    def event_handler(self, events: list[pygame.event.Event]):
        if self.active:
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    self.current_selection_index = (self.current_selection_index + 1) % len(self.options)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    self.current_selection_index = (self.current_selection_index - 1) if self.current_selection_index > 0 else len(self.options) - 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if self.return_options[self.current_selection_index]:
                        return self.return_options[self.current_selection_index]

