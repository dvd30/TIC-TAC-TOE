import pygame
import sys

height = 300
width = 300
dimension = 3
cell_size = width//dimension
start_img = pygame.image.load(r'C:\Users\Divyanshu\Downloads\start.png')
score_o = 0
score_x = 0


class Game:
    def __init__(self):
        self.board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        self.player_1 = True
        self.playable_moves = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        self.font1 = pygame.font.Font("freesansbold.ttf", 32)
        self.font2 = pygame.font.Font("freesansbold.ttf", 24)

    def move(self, draw):
        if self.player_1:
            self.board[draw.row][draw.col] = '1'
            self.player_1 = not self.player_1
        else:
            self.board[draw.row][draw.col] = '2'
            self.player_1 = not self.player_1

    def win(self, player, screen):
        # horizontal win
        for c in range(dimension):
            if self.board[0][c] == player and self.board[1][c] == player and self.board[2][c] == player:
                self.draw_horizontal_win_line(c, screen)
                return True
        # vertical win
        for r in range(dimension):
            if self.board[r][0] == player and self.board[r][1] == player and self.board[r][2] == player:
                self.draw_vertical_win_line(r, screen)
                return True
        # diagonal Win
        if self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player:
            self.draw_diagonal_win_line(screen)
            return True
        # other wins
        if self.board[0][2] == player and self.board[1][1] == player and self.board[2][0] == player:
            self.draw_other_diagonal_win_line(screen)
            return True

        return False

    def draw_vertical_win_line(self, c, screen):
        r = c*100+50
        color = (255, 255, 255) if self.player_1 is False else (64, 64, 64)
        pygame.draw.line(screen, color, (r, c), (r, height), 5)

    def draw_horizontal_win_line(self, r, screen):
        c = r*100+50
        color = (255, 255, 255) if self.player_1 is False else (64, 64, 64)
        pygame.draw.line(screen, color, (r, c), (width, c), 5)

    def draw_diagonal_win_line(self, screen):
        color = (255, 255, 255) if self.player_1 is False else (64, 64, 64)
        pygame.draw.line(screen, color, (0, 0), (height, width), 5)

    def draw_other_diagonal_win_line(self, screen):
        color = (255, 255, 255) if self.player_1 is False else (64, 64, 64)
        pygame.draw.line(screen, color, (0, width), (height, 0), 5)


class Draw:
    def __init__(self, selected_row, selected_col):
        self.row = selected_row
        self.col = selected_col


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self, screen, destination):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                destination()
                self.clicked = True
        screen.blit(self.image, self.rect)
        return True


def start():
    pygame.init()
    screen = pygame.display.set_mode((height, width))
    game = Game()
    pygame.display.set_caption("TIC-TAC-TOE")
    restart = game.font2.render("Press 'r' to Restart", True, (255, 255, 255))
    score = game.font2.render("Press 's' for Scores", True, (255, 255, 255))
    head = game.font1.render("TIC-TAC-TOE", True, (255, 255, 255))
    start_button = Button(110, 100, start_img)
    screen.fill((28, 170, 156))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    scores()
        screen.blit(head, (55, 50))
        screen.blit(restart, (40, 180))
        screen.blit(score, (40, 210))
        start_button.draw(screen, main)
        pygame.display.update()


def main():
    global score_o, score_x
    pygame.init()
    screen = pygame.display.set_mode((height, width))
    pygame.display.set_caption("TIC-TAC-TOE")
    game = Game()
    screen.fill((28, 170, 156))
    draw_board(screen)
    game_over = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                location = pygame.mouse.get_pos()
                r = location[0]//cell_size
                c = location[1]//cell_size
                position_selected = (r, c)
                if position_selected == (r, c):
                    draw = Draw(r, c)
                    if position_selected in game.playable_moves:
                        game.move(draw)
                        print(position_selected)
                        game.playable_moves.remove(position_selected)
                        if game.board[r][c] == '1':
                            player1(screen, r, c)
                            game.win("1", screen)
                            if game.win("1", screen):
                                game_over = True
                                winner = game.font1.render("Player 1 Wins", True, (255, 255, 255))
                                screen.blit(winner, (width/2-100, height/2-10))
                                score_o += 1
                            elif not game.playable_moves and not game.win("1", screen):
                                game_over = True
                                winner = game.font1.render("DRAW", True, (255, 255, 255))
                                screen.blit(winner, (width / 2 - 50, height / 2 - 10))

                        elif game.board[r][c] == '2':
                            player2(screen, r, c)
                            game.win("2", screen)
                            if game.win("2", screen):
                                game_over = True
                                winner = game.font1.render("Player 2 Wins", True, (64, 64, 64))
                                screen.blit(winner, (width/2-100, height/2-10))
                                score_x += 1
                            elif not game.playable_moves and not game.win("2", screen):
                                game_over = True
                                winner = game.font1.render("DRAW", True, (255, 255, 255))
                                screen.blit(winner, (width / 2 - 50, height / 2 - 10))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    scores()
                if event.key == pygame.K_r:
                    main()
        pygame.display.update()


def scores():
    global score_o, score_x
    pygame.init()
    screen = pygame.display.set_mode((height, width))
    pygame.display.set_caption("TIC-TAC-TOE")
    game = Game()
    score = game.font1.render("Scores", True, (255, 255, 255))
    score_o_player1 = game.font2.render(f"Player o: {score_o}", True, (255, 255, 255))
    score_x_player2 = game.font2.render(f"Player x: {score_x}", True, (255, 255, 255))
    to_start = game.font2.render("Press 'm' for main menu", True, (255, 255, 255))
    to_game = game.font2.render("Press 'g' to play", True, (255, 255, 255))

    screen.fill((28, 170, 156))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    start()
                if event.key == pygame.K_g:
                    main()
        screen.blit(score, (90, 50))
        screen.blit(score_o_player1, (50, 100))
        screen.blit(score_x_player2, (50, 150))
        screen.blit(to_game, (40, 200))
        screen.blit(to_start, (10, 250))
        pygame.display.update()


def draw_board(screen):
    for i in range(1, dimension):
        pygame.draw.line(screen, (23, 145, 135), (0, cell_size * i), (width, cell_size * i), 5)
        pygame.draw.line(screen, (23, 145, 135), (cell_size * i, 0), (cell_size * i, height), 5)


def player1(screen, r, c):
    pygame.draw.circle(screen, (255, 255, 255), (((r*cell_size)+cell_size/2), ((c*cell_size)+cell_size/2)),
                       cell_size/2-10, 8)


def player2(screen, r, c):
    pygame.draw.line(screen, (64, 64, 64), ((r*cell_size)+10,
                                            ((c+1)*cell_size)-10), (((r+1)*cell_size)-10, (c*cell_size)+10), 10)
    pygame.draw.line(screen, (64, 64, 64), ((r*cell_size)+10, (c*cell_size)+10), (((r+1)*cell_size)-10,
                                                                                  ((c+1)*cell_size)-10), 10)


def draw_move(screen, board):
    for r in range(0, dimension-1):
        for c in range(0, dimension-1):
            chance = board[r][c]
            if chance == '1':
                player1(screen, r, c)
            elif chance == '2':
                player2(screen, r, c)


if __name__ == '__main__':
    start()
