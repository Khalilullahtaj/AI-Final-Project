import pygame
import sys
import time
import tictactoe as tic

pygame.init()

# Window configuration
size = (600, 500)
screen = pygame.display.set_mode(size)
LIGHT_BLUE = (173, 216, 230)  
NAVY_BLUE = (0, 0, 128)  
YELLOW = (255, 255, 0)  


medium_font = pygame.font.Font("OpenSans-Regular.ttf", 30)
large_font = pygame.font.Font("OpenSans-Regular.ttf", 42)
move_font = pygame.font.Font("OpenSans-Regular.ttf", 62)

# Initial game state
player_side = None
board = tic.initial_state()
ai_turn = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(LIGHT_BLUE)

    if player_side is None:
        # Draw title
        title = large_font.render("I love Tic-Tac-Toe!", True, NAVY_BLUE)
        title_rect = title.get_rect(center=(size[0] / 2, 50))
        screen.blit(title, title_rect)

        # Buttons for choosing player
        play_x_button = pygame.Rect(size[0] / 8, size[1] / 2, size[0] / 4, 50)
        play_o_button = pygame.Rect(5 * size[0] / 8, size[1] / 2, size[0] / 4, 50)

        # Draw buttons and check click events
        for button, role in [(play_x_button, tic.X), (play_o_button, tic.O)]:
            pygame.draw.rect(screen, NAVY_BLUE, button)
            label = medium_font.render(f"Play as {role}", True, YELLOW)
            label_rect = label.get_rect(center=button.center)
            screen.blit(label, label_rect)

            if pygame.mouse.get_pressed()[0]:
                if button.collidepoint(pygame.mouse.get_pos()):
                    time.sleep(0.2)  # Debounce the button click
                    player_side = role

    else:
        # Draw the game board
        tile_size = 110
        tile_origin = (size[0] / 2 - 1.5 * tile_size, size[1] / 2 - 1.5 * tile_size)
        tiles = []

        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(tile_origin[0] + j * tile_size, tile_origin[1] + i * tile_size, tile_size, tile_size)
                pygame.draw.rect(screen, NAVY_BLUE, rect, 3)

                if board[i][j] is not tic.EMPTY:
                    move = move_font.render(board[i][j], True, YELLOW)
                    move_rect = move.get_rect(center=rect.center)
                    screen.blit(move, move_rect)
                row.append(rect)
            tiles.append(row)

        # Game status updates
        game_over = tic.terminal(board)
        current_player = tic.player(board)

        # Display status message
        if game_over:
            winner = tic.winner(board)
            title_text = f"Congrats {winner}!" if winner else "Game is tie!"
        else:
            title_text = f"Player {current_player}'s turn" if player_side == current_player else "Let me think :)"
        title = large_font.render(title_text, True, "red")
        title_rect = title.get_rect(center=(size[0] / 2, 30))
        screen.blit(title, title_rect)

        # AI move logic
        if player_side != current_player and not game_over:
            if ai_turn:
                time.sleep(0.5)  # Delay for AI 'thinking'
                move = tic.minimax(board)
                board = tic.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Player move logic
        if pygame.mouse.get_pressed()[0] and player_side == current_player and not game_over:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if board[i][j] == tic.EMPTY and tiles[i][j].collidepoint(mouse_pos):
                        board = tic.result(board, (i, j))

        # Play again logic
        if game_over:
            again_button = pygame.Rect(size[0] / 3, size[1] - 65, size[0] / 3, 50)
            again = medium_font.render("Restart", True, YELLOW)
            again_rect = again.get_rect(center=again_button.center)
            pygame.draw.rect(screen, NAVY_BLUE, again_button)
            screen.blit(again, again_rect)

            if pygame.mouse.get_pressed()[0] and again_button.collidepoint(pygame.mouse.get_pos()):
                time.sleep(0.2)
                player_side = None
                board = tic.initial_state()
                ai_turn = False

    pygame.display.flip()
