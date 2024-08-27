import csv
import os

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.score = 0

class OthelloGame:
    def __init__(self):
        self.players = []
        self.board_size = 8
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        self.current_player_idx = 0

    def show_menu(self):
        print("1. 게임을 시작한다.")
        print("2. 플레이어 전적")
        print("0. 게임 종료")
        choice = input("선택: ")
        return choice

    def start_game(self):
        num_players = int(input("플레이어 수를 정하세요 (2, 3, 4명): "))
        self.setup_players(num_players)
        self.initialize_board()
        self.play_game()
        self.save_results()
        self.reset_game()

    def setup_players(self, num_players):
        colors = {
            2: ["흰색", "검정색"],
            3: ["빨강", "파랑", "초록"],
            4: ["빨강", "파랑", "초록", "노랑"]
        }
        for i in range(num_players):
            name = input(f"플레이어 {i + 1} 이름: ")
            player = Player(name, colors[num_players][i])
            self.players.append(player)

    def initialize_board(self):
        mid = self.board_size // 2
        self.board[mid - 1][mid - 1] = 'W'
        self.board[mid - 1][mid] = 'B'
        self.board[mid][mid - 1] = 'B'
        self.board[mid][mid] = 'W'

    def print_board(self):
        print("  " + " ".join(str(i) for i in range(self.board_size)))
        for i in range(self.board_size):
            print(f"{i} " + " ".join(self.board[i]))

    def play_game(self):
        consecutive_passes = 0
        
        while consecutive_passes < len(self.players):
            self.print_board()
            current_player = self.players[self.current_player_idx]
            print(f"{current_player.name} ({current_player.color}) 차례입니다.")
            
            if self.has_valid_move(current_player.color):
                row, col = map(int, input("놓을 위치 (row col): ").split())
                if self.is_valid_move(row, col, current_player.color):
                    self.place_stone(row, col, current_player.color)
                    consecutive_passes = 0
                else:
                    print("잘못된 위치입니다. 다시 시도하세요.")
                    continue
            else:
                print(f"{current_player.name}는 놓을 수 있는 자리가 없습니다. 패스합니다.")
                consecutive_passes += 1
            
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        
        winner = self.calculate_winner()
        if winner:
            winner.score += 1
            print(f"{winner.name} ({winner.color})이 승리했습니다!")
        else:
            print("무승부입니다!")

    def has_valid_move(self, color):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.is_valid_move(row, col, color):
                    return True
        return False

    def is_valid_move(self, row, col, color):
        if self.board[row][col] != ' ':
            return False
        
        for direction in self.directions:
            if self.can_flip(row, col, direction, color):
                return True
        return False

    def can_flip(self, row, col, direction, color):
        dx, dy = direction
        x, y = row + dx, col + dy
        opponent_color = 'B' if color == 'W' else 'W'
        
        has_opponent_stone = False
        
        while 0 <= x < self.board_size and 0 <= y < self.board_size:
            if self.board[x][y] == opponent_color:
                has_opponent_stone = True
                x += dx
                y += dy
            elif self.board[x][y] == color:
                return has_opponent_stone
            else:
                break
        
        return False

    def place_stone(self, row, col, color):
        self.board[row][col] = color
        for direction in self.directions:
            if self.can_flip(row, col, direction, color):
                self.flip_stones(row, col, direction, color)

    def flip_stones(self, row, col, direction, color):
        dx, dy = direction
        x, y = row + dx, col + dy
        opponent_color = 'B' if color == 'W' else 'W'
        
        while self.board[x][y] == opponent_color:
            self.board[x][y] = color
            x += dx
            y += dy

    def is_game_over(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                for player in self.players:
                    if self.is_valid_move(row, col, player.color):
                        return False
        return True

    def calculate_winner(self):
        black_count = sum(row.count('B') for row in self.board)
        white_count = sum(row.count('W') for row in self.board)
        
        if black_count > white_count:
            return self.players[1]  # 검정색 플레이어가 승리
        elif white_count > black_count:
            return self.players[0]  # 흰색 플레이어가 승리
        else:
            return None  # 무승부

    def save_results(self):
        file_exists = os.path.isfile('sav.csv')
        with open('sav.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["이름", "색깔", "전적"])
            for player in self.players:
                writer.writerow([player.name, player.color, player.score])

    def view_stats(self):
        if not os.path.isfile('sav.csv'):
            print("플레이어가 없습니다.")
            return
        
        player_stats = {}
        with open('sav.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # 헤더 스킵
            for row in reader:
                name, color, score = row
                score = int(score)
                if name in player_stats:
                    player_stats[name]['games'] += 1
                    player_stats[name]['wins'] += score
                else:
                    player_stats[name] = {'games': 1, 'wins': score}

        for name, stats in player_stats.items():
            games = stats['games']
            wins = stats['wins']
            win_rate = (wins / games) * 100 if games > 0 else 0
            print(f"플레이어: {name}, 승리: {wins}, 게임 수: {games}, 승률: {win_rate:.2f}%")

    def reset_game(self):
        self.players = []
        self.board = [[' ' for _ in range(self.board_size)]]

    def run(self):
        while True:
            choice = self.show_menu()
            if choice == '1':
                self.start_game()
            elif choice == '2':
                self.view_stats()
            elif choice == '0':
                print("게임을 종료합니다.")
                break
            else:
                print("잘못된 선택입니다. 다시 시도해주세요.")

if __name__ == "__main__":
    game = OthelloGame()
    game.run()
