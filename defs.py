import time
import os

offset =  [ [-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1] ]


def boardPrint(gameBoard, N):
    os.system('clear')
    print("<Othello Game>")
    print("X", end="")
    for i in range(1, N+1):
        print("",i, end="")
    print()
    for i in range(1, N+1):
        print(i, end="")
        # 세로 열 출력
        for j in range(1, N+1):
            print(" " + gameBoard[j][i], end="")
        print()
    time.sleep(0.3)


def gameOver(cnt, imp, N):
    if(cnt[0] == N*N or cnt[1] == 0 or cnt[2] == 0 or imp == 2):
        return 1
    return 0
# cnt[0] : 전체 돌의 개수
# cnt[1] : 검은 돌의 개수
# cnt[2] : 흰 돌의 개수


def colorChange(color):
    if color == '○':
        return '●'
    else:
        return '○'


def areaCheck(row, col, N):
    if (1 <= row <= N+1) and (1 <= col <= N+1):
        return 1 # 영역 안에 있을 때
    else:
        return 0 # 영역 밖에 있을 때
    

def misPlace(gameBoard, color, row, col, N):
    if (not areaCheck(row, col, N)) or (not gameBoard[row][col] == '□'):
    # 영역 밖에 있거나 빈자리가 아니거나
        return 1
    
    oppColor = colorChange(color)

    for i in range(0, 8): # 8방향
        roww = row + offset[i][0]
        coll = col + offset[i][1]

        while gameBoard[roww][coll] == oppColor:
            roww += offset[i][0]
            coll += offset[i][1]

            if gameBoard[roww][coll] == color: # 상대돌이 끝나고 자신이 돌이 나올 때
                return 0
        
    return 1 # 다 해보고도 안 되었을 때


def imposBoard(gameBoard, color, N):
    for i in range(1, N+1):
        for j in range(1, N+1):
            if gameBoard[i][j] == '□':
                if not misPlace(gameBoard, color, i, j, N):
                    return 0
    return 1 # 다 해보고도 안 되었을 때


def moving(gameBoard, color, row, col, cnt, N):
    offCnt = [0 for i in range(8)] # 8방향
    count = 0
    sum = 0
    roww = coll = -1
    oppColor = colorChange(color)
    gameBoard[row][col] = color

    for i in range(0, 8):  # 8방향
        roww = row + offset[i][0]
        coll = col + offset[i][1]
        count = 0

        while gameBoard[roww][coll] == oppColor: # offset 위치에 상대돌이 존재할 때
            roww += offset[i][0]
            coll += offset[i][1]
            count += 1
                
        if gameBoard[roww][coll] == '□': # 가장자리이거나 빈자리면 안 됨
            count = 0
        
        offCnt[i] = count
        sum += count
        # 자신과 같은 색의 돌일 때
    
    # 색에 따라서 cnt를 바꾸는 코드
    cnt[0] += 1
    if color == '●':
        cnt[1] += (sum + 1)
        cnt[2] -= sum
    else:
        cnt[2] += (sum + 1)
        cnt[1] -= sum

    boardPrint(gameBoard, N) # 돌 놓은 위치부터 시작.

    for i in range(1, N): # 최대 (N-1)번까지 연속으로 뒤집을 수 있기 때문
        if sum > 0:
            for j in range(0, 8): # 8방향
                if offCnt[j] > 0:
                    gameBoard[row + i*offset[j][0]][col + i*offset[j][1]] = color
                    offCnt[j] -= 1
                    sum -= 1
            boardPrint(gameBoard, N)


def resultPrint(cnt):
    if cnt[1] > cnt[2]:
        print("●:", cnt[1], "\n○:", cnt[2], "\nWINNNER : BLACK!")
    elif cnt[1] < cnt[2]:
        print("●:", cnt[1], "\n○:", cnt[2], "\nWINNNER : WHITE!")
    else:
        print("●:", cnt[1], "\n○:", cnt[2], "\nDRAW!")
        
