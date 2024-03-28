import sys
import warnings
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

warnings.filterwarnings("ignore", category=DeprecationWarning)

BOARD_SIZE = 3
EMPTY_CELL = 0
HUMAN_PLAYER = 1
AI_PLAYER = 2

def evaluate_board(board):
    #check rows
    for row in board:
        if row.count(HUMAN_PLAYER) == 3:
            return -1
        elif row.count(AI_PLAYER) == 3:
            return 1
        
    #Check columns
    for col in range(BOARD_SIZE):
        if [board[row][col] for row in range(BOARD_SIZE)].count(HUMAN_PLAYER) == 3:
            return -1
        elif [board[row][col] for row in range(BOARD_SIZE)].count(AI_PLAYER) == 3:
            return 1

    #Check diagonals
    if [board[i][i] for i in range(BOARD_SIZE)].count(HUMAN_PLAYER) == 3 or \
       [board[i][BOARD_SIZE - i - 1] for i in range(BOARD_SIZE)].count(HUMAN_PLAYER) == 3:
        return -1
    elif [board[i][i] for i in range(BOARD_SIZE)].count(AI_PLAYER) == 3 or \
         [board[i][BOARD_SIZE - i - 1] for i in range(BOARD_SIZE)].count(AI_PLAYER) == 3:
        return 1

    if sum([row.count(EMPTY_CELL) for row in board]) == 0:
        return 0

    return None

def minimax(board, depth, is_maximizing, alpha, beta):
    score = evaluate_board(board)
    if score is not None:
        return score

    if is_maximizing:
        best_score = -sys.maxsize
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == EMPTY_CELL:
                    board[row][col] = AI_PLAYER
                    score = minimax(board, depth + 1, False, alpha, beta)
                    board[row][col] = EMPTY_CELL
                    best_score = max(best_score, score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break  
        return best_score

    else:
        best_score = sys.maxsize
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == EMPTY_CELL:
                    board[row][col] = HUMAN_PLAYER
                    score = minimax(board, depth + 1, True, alpha, beta)
                    board[row][col] = EMPTY_CELL
                    best_score = min(best_score, score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break  
        return best_score


def get_ai_move(board):
    best_score = -sys.maxsize
    best_move = None
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == EMPTY_CELL:
                board[row][col] = AI_PLAYER
                score = minimax(board, 0, False, -sys.maxsize, sys.maxsize)
                board[row][col] = EMPTY_CELL
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    return best_move


class Main_UI(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("F:\\Python\\codsoft\\tictactoe\\TTT.ui", self)
        self.setWindowTitle("Tic Tac Toe")
        
        self.turns = 0
        self.counter = 0
        self.board = [[EMPTY_CELL] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        self.B1.clicked.connect(lambda: self.Buttons("B1"))
        self.B2.clicked.connect(lambda: self.Buttons("B2"))
        self.B3.clicked.connect(lambda: self.Buttons("B3"))
        self.B4.clicked.connect(lambda: self.Buttons("B4"))
        self.B5.clicked.connect(lambda: self.Buttons("B5"))
        self.B6.clicked.connect(lambda: self.Buttons("B6"))
        self.B7.clicked.connect(lambda: self.Buttons("B7"))
        self.B8.clicked.connect(lambda: self.Buttons("B8"))
        self.B9.clicked.connect(lambda: self.Buttons("B9"))
        
        self.toolButton_10.clicked.connect(lambda: self.restart())
        self.setWindowIcon(QtGui.QIcon('F:\\Python\\codsoft\\tictactoe\\logo.png'))
        self.setWindowFlags(self.windowFlags() | Qt.MSWindowsFixedSizeDialogHint)
    def restart(self):
        self.turns = 0
        self.counter = 0
        self.board = [[EMPTY_CELL] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.label.setStyleSheet("color: #55aaff")
        self.label.setText("Let's play again!")
        self.enable_buttons()


        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                getattr(self, "B" + str(row * 3 + col + 1)).setText("")

    def Buttons(self, event):
        button_map = {
            "B1": (0, 0), "B2": (0, 1), "B3": (0, 2),
            "B4": (1, 0), "B5": (1, 1), "B6": (1, 2),
            "B7": (2, 0), "B8": (2, 1), "B9": (2, 2)
        }
        row, col = button_map[event]

        if self.board[row][col] != EMPTY_CELL:
            return
        
        if self.turns == 0:
            self.board[row][col] = HUMAN_PLAYER
            getattr(self, event).setText("X")
            self.turns += 1
        else:
            return
        
        winner = evaluate_board(self.board)
        if winner is not None:
            if winner == 0:
                self.label.setStyleSheet("color: #55aaff;")
                self.label.setText("Match Draw :(")
            elif winner == 1:
                self.label.setStyleSheet("color: #55aaff")
                self.label.setText("Hurray! You won!")
            else:
                self.label.setStyleSheet("color: #55aaff")
                self.label.setText("The AI has won..")
            self.Button_Disabled()
            return
        
        self.label.setStyleSheet("color: #55aaff")
        self.label.setText("The AI is thinking...")

        QtCore.QTimer.singleShot(1000, self.ai_move)

    def ai_move(self):
        ai_move = get_ai_move(self.board)
        if ai_move:
            row, col = ai_move
            self.board[row][col] = AI_PLAYER
            getattr(self, "B" + str(row * 3 + col + 1)).setText("0") 
            self.turns -= 1

            winner = evaluate_board(self.board)
            if winner is not None:
                if winner == 0:
                    self.label.setStyleSheet("color: #55aaff")
                    self.label.setText("Match Draw :(")
                elif winner == 1:
                    self.label.setStyleSheet("color: #55aaff")
                    self.label.setText("The AI has won...")
                else:
                    self.label.setStyleSheet("color: #55aaff")
                    self.label.setText("Hurray! You won!")
                self.Button_Disabled()
            else:
                self.label.setStyleSheet("color: #55aaff")
                self.label.setText("Your turn!")

        self.counter += 1

    def Button_Disabled(self):
        self.B1.setEnabled(False)
        self.B2.setEnabled(False)
        self.B3.setEnabled(False)
        self.B4.setEnabled(False)
        self.B5.setEnabled(False)
        self.B6.setEnabled(False)
        self.B7.setEnabled(False)
        self.B8.setEnabled(False)
        self.B9.setEnabled(False)

    def enable_buttons(self):
        self.B1.setEnabled(True)
        self.B2.setEnabled(True)
        self.B3.setEnabled(True)
        self.B4.setEnabled(True)
        self.B5.setEnabled(True)
        self.B6.setEnabled(True)
        self.B7.setEnabled(True)
        self.B8.setEnabled(True)
        self.B9.setEnabled(True)


def main():
    try:
        MainApp = QtWidgets.QApplication(sys.argv)
        App = Main_UI()
        App.show()
        exit_code = MainApp.exec_()
        sys.exit(exit_code)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()