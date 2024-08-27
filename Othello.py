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
        current_player_idx = 0
        while not self.is_game_over():
            self.print_board()
            current_player = self.players[current_player_idx]
            print(f"{current_player.name} ({current_player.color}) 차례입니다.")
            row, col = map(int, input("놓을 위치 (row col): ").split())
            if self.is_valid_move(row, col, current_player.color):
                self.place_stone(row, col, current_player.color)
                current_player_idx = (current_player_idx + 1) % len(self.players)
            else:
                print("잘못된 위치입니다. 다시 시도하세요.")
        
        winner = self.calculate_winner()
        winner.score += 1
        print(f"{winner.name} ({winner.color})이 승리했습니다!")

    def is_valid_move(self, row, col, color):
        # 간단한 유효성 검사 (빈 칸에 놓을 수 있는지 확인)
        if self.board[row][col] != ' ':
            return False
        # 추가로 돌을 뒤집을 수 있는지 확인하는 로직 필요
        return True

    def place_stone(self, row, col, color):
        self.board[row][col] = color
        # 돌 뒤집는 로직 추가 필요

    def is_game_over(self):
        # 게임이 끝났는지 확인하는 로직 필요
        return False

    def calculate_winner(self):
        # 승자를 결정하는 로직 구현 (예시로 첫 번째 플레이어 승리)
        return self.players[0]

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
