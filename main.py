from SpeedTypingApp import SpeedTypingApp
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

running = True
game = SpeedTypingApp(screen)
game.run_game()

pygame.quit()
