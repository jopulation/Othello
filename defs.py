import time
offset =  [ [-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1] ]


def boardPrint(gameBoard):
    print("X 1 2 3 4 5 6 7 8")
    for i in range(1, 9):
        print(i, end="")
        # 세로 열 출력
        for j in range(1, 9):
            print(" " + gameBoard[j][i], end="")
        print()

def gameOver(cnt):
    if(cnt[0] == 64 or cnt[1] == 0 or cnt[2] == 0):
        return 1
    return 0
# cnt[0] : 전체 돌의 개수
# cnt[1] : 검은 돌의 개수
# cnt[2] : 흰 돌의 개수

def colorchange(color):
    if color == '○':
        return '●'
    else:
        return '○'
    
def imposBoard(gameBoard, color):
    oppcolor = colorchange(color)

    for i in range(1, 9):
        for j in range(1, 9):
            if color == gameBoard[i][j]:

                for k in range(0, 8):
                    roww = i + offset[k][0]
                    coll = j + offset[k][1]

                    if oppcolor == gameBoard[roww][coll]:
                        while not gameBoard[roww][coll] == ' ': # 가장자리이거나 빈자리이거나
                            roww += offset[k][0]
                            coll += offset[k][1]

                            if gameBoard[roww][coll] == color: # 자신과 같은 색의 돌이면 안 됨
                                break
                        if roww == 0 or roww == 9 or coll == 0 or coll == 9:
                            break #가장자리일 때
                        return 0 # 놓을 수 있는 빈자리가 있을 때
    return 1


def areaCheck(row, col):
    if (1 <= row <=9) and (1 <= col <= 9):
        return 1 # 영역 안에 있을 때
    else:
        return 0 # 영역 밖에 있을 때
    

def misPlace(gameBoard, color, row, col):
    if (not areaCheck(row, col)) or (not gameBoard[row][col] == ' '):
    # 영역 밖에 있거나 빈자리
        return 1
    
    oppColor = colorchange(color)
    roww = coll = -1 # 초기화

    for i in range(0,8):
        roww = row + offset[i][0]
        coll = col + offset[i][1]

        if oppColor == gameBoard[roww][coll]:
            while not gameBoard[roww][coll] == color: # 자신과 같은 돌일 때
                roww += offset[i][0]
                coll += offset[i][1]
                
                if gameBoard[roww][coll] == ' ': # 가장자리이거나 빈자리이면 안 됨
                    continue
            return 0 # 자신과 같은 색의 돌일 때
    return 1 # 다 해보고도  안 되었을 때

def moving(gameBoard, color, row, col, cnt):
    offCnt = [0 for i in range(8)]
    count = 0
    sum = 0
    roww = coll = -1
    oppColor = colorchange(color)

    for i in range(0, 8):
        roww = i + offset[i][0]
        coll = i + offset[i][1]
        count = 1

        if oppColor == gameBoard[roww][coll]:
            while not  gameBoard[roww][coll] == color:
                roww += offset[i][0]
                coll += offset[i][1]
                ++count

                if gameBoard[roww][coll] == ' ': # 가장자리이거나 빈자리면 안 됨
                    break
        offCnt[i] = count
        sum += count
        # 자신과 같은 색의 돌일 때
    # 색에 따라서 cnt를 바꾸는 코드
    ++cnt[0]
    if color == '●':
        cnt[1] += sum
        cnt[2] -= sum
    else:
        cnt[2] += sum
        cnt[1] -= sum

    while sum > 0:
        for i in range(1, 8): # 최대 7번까지 연속으로 뒤집을 수 있기 때문
            for j in range(0, 8):
                if offCnt[j] > 0:
                    gameBoard[row + i*offset[j][0]][col + i*offset[j][1]] = color
                    --offCnt[j]
                    --sum
            boardPrint(gameBoard)
            time.sleep(1)






def resultPrint(cnt):
    if cnt[1] > cnt[2]:
        print("WINNNER : BLACK!", end ="")
    elif cnt[1] < cnt[2]:
        print("WINNNER : WHITE!", end ="")
    else:
        print("DRAW!", end="")
