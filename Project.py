import pygame
import sys


board = Board()

pygame.init()

# Constants
BOARD_SIZE = 8
SQUARE_SIZE = 64
WINDOW_SIZE = BOARD_SIZE * SQUARE_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

board_width = 800  # Replace with the actual width of your board
board_height = 800  # Replace with the actual height of your board
squares_per_row = 8
squares_per_column = 8

square_width = WINDOW_SIZE // squares_per_row
square_height = WINDOW_SIZE // squares_per_column


piece_images = {}

def add_background_color(image, background_color=(255, 255, 255, 100)):
    new_image = pygame.Surface((image.get_width(), image.get_height()), pygame.SRCALPHA)
    new_image.fill(background_color)
    new_image.blit(image, (0, 0))
    return new_image

for color in ['white', 'black']:
    for piece_type in ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']:
        key = f"{piece_type}_{color}"
        img_path = f"{piece_type}_{color}.png"  # Make sure this path points to the correct image file
        original_img = pygame.image.load(img_path)
        scaled_img = pygame.transform.scale(original_img, (square_width, square_height))
        if color == 'black':
            scaled_img = add_background_color(scaled_img, background_color=(255, 255, 255, 100))
        piece_images[key] = scaled_img


# Initialize the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Chess Game")

def draw_board():
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            rect = pygame.Rect(x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, WHITE if (x + y) % 2 == 0 else BLACK, rect)

            piece = board.board[y][x]
            if piece:
                img = piece_images[f"{piece.piece_type}_{piece.color}"]
                screen.blit(img, rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    draw_board()
    pygame.display.update()

