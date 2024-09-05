def boardPrint(gameBoard):
    print("X 1 2 3 4 5 6 7 8")
    for i in range(1, 9):
        print(i, end="")
        # 세로 열 출력
        for j in range(1, 9):
            print(" " + gameBoard[j][i], end="")
        print()
