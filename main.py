import defs

# gameBoard[row][col]
# 게임보드 초기상태
gameBoard = [['□']*10 for i in range(10)]
gameBoard[4][4] = gameBoard[5][5] = '○'
gameBoard[4][5] = gameBoard[5][4] = '●'

row = col = -1
cnt = [ 4, 2, 2]
# cnt[0] : 전체 돌의 개수
# cnt[1] : 검은 돌의 개수
# cnt[2] : 흰 돌의 개수
color = '●' # 검은돌로 시작

#Othello Game
defs.boardPrint(gameBoard)
while not defs.gameOver(cnt):
    if defs.imposBoard(gameBoard, color): # 놓을 수 없는 경우
        print(color + "은 놓을 수 있는 곳이 없습니다.")
        color = defs.colorChange(color)

    else: # 놓을 수 있는 경우
        while True:
            try:
                row, col = map(int, input(color + "차례>\n놓을 곳을 입력해주세요->").split())
                # 숫자가 아닌 경우 예외처리(필요)
                break
            except:
                print('입력이 정확하지 않습니다.')

        # 잘못 놓았을 경우
        while True:
            try:
                while defs.misPlace(gameBoard, color, row, col):
                    row, col = map(int, input("놓을 수 없는 곳입니다.\n다시 입력해주세요. 예시: 1 8 ->").split())
                break
            except:
                print('입력이 정확하지 않습니다.')

        defs.moving(gameBoard, color, row, col, cnt)
        color = defs.colorChange(color) # 턴 마치고 색 바꾸기

defs.resultPrint(cnt)
