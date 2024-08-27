import pygame
import sys

# 색상 정의
colors = {
    2: [(255, 0, 0), (0, 255, 0)],  # 빨강, 초록
    3: [(255, 0, 0), (0, 255, 0), (128, 0, 128)],  # 빨강, 초록, 보라
    4: [(255, 0, 0), (0, 255, 0), (128, 0, 128), (255, 255, 0)]  # 빨강, 초록, 보라, 노랑
}

# 기본 설정
pygame.init()

# 화면 크기 설정
board_size = 8
screen_size = 640
cell_size = screen_size // board_size

# 화면 생성
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption('오셀로 게임')

# 방향 정의 (8방향)
directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

# 게임보드 초기화
def initialize_board():
    board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
    mid = board_size // 2
    board[mid - 1][mid - 1] = 'R'  # Red
    board[mid - 1][mid] = 'G'  # Green
    board[mid][mid - 1] = 'G'  # Green
    board[mid][mid] = 'R'  # Red
    return board

# 게임보드 그리기
def draw_board(board):
    screen.fill((0, 0, 0))
    for row in range(board_size):
        for col in range(board_size):
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)

            # 돌 그리기
            if board[row][col] != ' ':
                color_idx = 'RGBY'.index(board[row][col])
                color = colors[len(colors)][color_idx]
                pygame.draw.circle(screen, color, rect.center, cell_size // 2 - 5)

# 돌을 놓는 함수
def place_stone(board, row, col, current_color):
    board[row][col] = current_color

# 유효한 위치인지 확인하는 함수
def is_valid_move(board, row, col, current_color):
    if board[row][col] != ' ':
        return False
    for direction in directions:
        if can_flip(board, row, col, direction, current_color):
            return True
    return False

# 돌을 뒤집을 수 있는지 확인
def can_flip(board, row, col, direction, current_color):
    opponent_color = get_opponent_color(current_color)
    x, y = row + direction[0], col + direction[1]
    has_opponent_stone = False

    while 0 <= x < board_size and 0 <= y < board_size:
        if board[x][y] == opponent_color:
            has_opponent_stone = True
            x += direction[0]
            y += direction[1]
        elif board[x][y] == current_color:
            return has_opponent_stone
        else:
            break
    return False

# 상대 돌의 색상 반환
def get_opponent_color(current_color):
    color_order = 'RGBY'
    idx = color_order.index(current_color)
    return color_order[(idx + 1) % len(color_order)]

# 돌 뒤집기
def flip_stones(board, row, col, current_color):
    for direction in directions:
        if can_flip(board, row, col, direction, current_color):
            x, y = row + direction[0], col + direction[1]
            while board[x][y] == get_opponent_color(current_color):
                board[x][y] = current_color
                x += direction[0]
                y += direction[1]

# 게임 종료 여부 확인
def is_game_over(board):
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] == ' ':
                return False
    return True

# 플레이어 순환
def get_next_player(current_idx, num_players):
    return (current_idx + 1) % num_players

# 플레이어의 돌이 모두 사라졌는지 확인
def has_no_stones(board, color):
    for row in board:
        if color in row:
            return False
    return True

# 검은 돌을 상대 돌과 인접한 빈 칸에 배치
def place_black_stone(board):
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] == ' ':
                for direction in directions:
                    x, y = row + direction[0], col + direction[1]
                    if 0 <= x < board_size and 0 <= y < board_size:
                        if board[x][y] != ' ':
                            board[row][col] = 'B'
                            return

# 승자 계산
def calculate_winner(board, player_colors):
    scores = {color: 0 for color in player_colors}
    for row in board:
        for stone in row:
            if stone in scores:
                scores[stone] += 1

    # 돌이 모두 사라진 플레이어는 승자 계산에서 제외
    for color in list(scores.keys()):
        if scores[color] == 0:
            del scores[color]

    # 최고 점수를 가진 플레이어가 승리
    winner = max(scores, key=scores.get)
    return winner, scores[winner]

def main():
    num_players = int(input("플레이어 수를 입력하세요 (2, 3, 4명): "))
    player_colors = 'RGBY'[:num_players]
    current_player_idx = 0
    current_color = player_colors[0]  # 첫 번째 플레이어는 빨간색으로 시작

    # 게임보드 초기화
    board = initialize_board()

    # 게임 루프
    running = True
    while running:
        draw_board(board)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                col = x // cell_size
                row = y // cell_size

                if is_valid_move(board, row, col, current_color):
                    place_stone(board, row, col, current_color)
                    flip_stones(board, row, col, current_color)

                    # 현재 플레이어의 돌이 모두 사라졌는지 확인
                    if has_no_stones(board, current_color):
                        print(f"{current_color} 플레이어의 돌이 모두 사라졌습니다.")
                        place_black_stone(board)

                    # 다음 플레이어로 전환
                    current_player_idx = get_next_player(current_player_idx, num_players)
                    current_color = player_colors[current_player_idx]

                    # 게임 종료 확인
                    if is_game_over(board):
                        print("게임 종료!")
                        winner, score = calculate_winner(board, player_colors)
                        print(f"{winner} 플레이어가 승리했습니다! 점수: {score}")
                        running = False
                        break

        pygame.time.Clock().tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
