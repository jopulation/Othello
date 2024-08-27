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

    def show_menu(self):
        print("1. 게임을 시작한다.")
        print("2. 플레이어 전적")
        print("0. 게임 종료")
        choice = input("선택: ")
        return choice

    def start_game(self):
        num_players = int(input("플레이어 수를 정하세요 (2, 3, 4명): "))
        self.setup_players(num_players)
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

    def play_game(self):
        # 오셀로 게임 로직 추가
        print("게임이 시작되었습니다!")
        # 예시 승자 설정
        winner = self.players[0]  # 첫 번째 플레이어가 승자라고 가정
        winner.score += 1  # 승자 점수 증가
        print(f"{winner.name}이 승리했습니다!")

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
        with open('sav.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)

    def reset_game(self):
        self.players = []

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
