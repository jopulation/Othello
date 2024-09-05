import defs

# gameBoard[row][col]
# 게임보드 초기상태
gameBoard = [['\0']*10 for i in range(10)]
gameBoard[4][4] = gameBoard[5][5] = '●'
gameBoard[4][5] = gameBoard[5][4] = '○'

row = col = -1


#Othello Game
print("<Othello Game>")
defs.boardPrint(gameBoard)
