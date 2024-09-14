import defs

N = 1 # N*N 형태의 보드판, N은 짝수
row = col = -1
color = '●' # 검은돌로 시작
imp = 0 # 양쪽 다 놓을 수 없는 경우를 찾기 위한 변수

#Othello Game
while not ( N%2 == 0 ) and ( N > 0 ) :
    try:
        N = int(input("보드판의 크기(짝수)를 입력하세요->"))
    except:
        print("입력이 정확하지 않습니다.")

# gameBoard[row][col]
# 게임보드 초기상태
gameBoard = [['□']*(N+2) for i in range(N+2)]
gameBoard[N//2][N//2] = gameBoard[N//2+1][N//2+1] = '○'
gameBoard[N//2][N//2+1] = gameBoard[N//2+1][N//2] = '●'

cnt = [ N, N//2, N//2]
# cnt[0] : 전체 돌의 개수
# cnt[1] : 검은 돌의 개수
# cnt[2] : 흰 돌의 개수

if N == 2:
    defs.boardPrint(gameBoard, N)
 
while not defs.gameOver(cnt, imp, N):
    posBoard = [['□']*(N+2) for i in range(N+2)] # 놓을 수 있는 자리 표시하는 보드판
    if defs.imposBoard(gameBoard, posBoard, color, N): # 놓을 수 없는 경우
        imp += 1
        print(color + "은 놓을 수 있는 곳이 없습니다.")
        color = defs.colorChange(color)
        defs.time.sleep(1)

    else: # 놓을 수 있는 경우
        imp = 0
        while True:
            try:
                defs.ableBoardPrint(gameBoard, posBoard, N)
                row, col = map(int, input(color + "차례>\n놓을 곳을 입력해주세요->").split())
                
                while defs.misPlace(gameBoard, color, row, col, N): # 잘못 놓았을 경우
                    defs.ableBoardPrint(gameBoard, posBoard, N)
                    row, col = map(int, input("놓을 수 없는 곳입니다.\n다시 입력해주세요. 예시: 1 8 ->").split())
                break
            except: # 입력값 예외처리
                print('입력이 정확하지 않습니다.')
                defs.time.sleep(1)

        defs.moving(gameBoard, color, row, col, cnt, N)
        color = defs.colorChange(color) # 턴 마치고 색 바꾸기

defs.resultPrint(cnt)
