import sys
import math

try:
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    from OpenGL.GLU import *
except ImportError:
    print("ERROR: PyOpenGL or GLUT not installed properly.")
    print("Please install PyOpenGL and PyOpenGL_accelerate:")
    print("  pip install PyOpenGL PyOpenGL_accelerate")
    print("And ensure GLUT (e.g., freeglut) is installed on your system.")
    sys.exit(1)

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 500
GRID_SIZE = 3
CELL_SIZE = WINDOW_WIDTH // GRID_SIZE
LINE_WIDTH = 5

EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2

COLOR_BACKGROUND = (0, 0, 0)
COLOR_LINES = (0.5, 0.5, 0.5)
COLOR_X = (0.2, 1, 0.2)
COLOR_O = (1, 0.2, 0.2)
COLOR_TEXT = (0, 1, 0)
COLOR_BUTTON = (0.7, 0.7, 0.7)
COLOR_BUTTON_TEXT = (0.0, 0.0, 0.0)

board = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
currentPlayer = PLAYER_X
gameOver = False
winner = None
message = "X's Turn"

button_rect = (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT - 60, 100, 40)

def draw_text(x, y, text_string, font_size=GLUT_BITMAP_HELVETICA_18, color=COLOR_TEXT):
    glColor3f(color[0], color[1], color[2])
    glRasterPos2f(x, y)
    for character in text_string:
        glutBitmapCharacter(font_size, ord(character))

def draw_grid():
    glColor3f(COLOR_LINES[0], COLOR_LINES[1], COLOR_LINES[2])
    glLineWidth(LINE_WIDTH)
    glBegin(GL_LINES)
    for i in range(1, GRID_SIZE):
        glVertex2f(i * CELL_SIZE, 0)
        glVertex2f(i * CELL_SIZE, GRID_SIZE * CELL_SIZE)
        glVertex2f(0, i * CELL_SIZE)
        glVertex2f(GRID_SIZE * CELL_SIZE, i * CELL_SIZE)
    glEnd()

def draw_X(center_x, center_y, size):
    glColor3f(COLOR_X[0], COLOR_X[1], COLOR_X[2])
    glLineWidth(LINE_WIDTH)
    half_size = size * 0.35
    glBegin(GL_LINES)
    glVertex2f(center_x - half_size, center_y - half_size)
    glVertex2f(center_x + half_size, center_y + half_size)
    glVertex2f(center_x - half_size, center_y + half_size)
    glVertex2f(center_x + half_size, center_y - half_size)
    glEnd()

def draw_O(center_x, center_y, radius):
    glColor3f(COLOR_O[0], COLOR_O[1], COLOR_O[2])
    glLineWidth(LINE_WIDTH)
    num_segments = 30
    glBegin(GL_LINE_LOOP)
    for i in range(num_segments):
        theta = 2.0 * 3.1415926 * float(i) / float(num_segments)
        x = radius * 0.7 * math.cos(theta)
        y = radius * 0.7 * math.sin(theta)
        glVertex2f(center_x + x, center_y + y)
    glEnd()

def draw_pieces():
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            center_x = c * CELL_SIZE + CELL_SIZE / 2
            center_y = r * CELL_SIZE + CELL_SIZE / 2
            if board[r][c] == PLAYER_X:
                draw_X(center_x, center_y, CELL_SIZE)
            elif board[r][c] == PLAYER_O:
                draw_O(center_x, center_y, CELL_SIZE / 2)

def draw_restart_button():
    bx, by, bw, bh = button_rect
    glColor3f(COLOR_BUTTON[0], COLOR_BUTTON[1], COLOR_BUTTON[2])
    glBegin(GL_QUADS)
    glVertex2f(bx, by)
    glVertex2f(bx + bw, by)
    glVertex2f(bx + bw, by + bh)
    glVertex2f(bx, by + bh)
    glEnd()
    draw_text(bx + 15, by + bh / 2 + 5, "Restart", color=COLOR_BUTTON_TEXT)

def reset_game():
    global board, currentPlayer, gameOver, winner, message
    board = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    currentPlayer = PLAYER_X
    gameOver = False
    winner = None
    message = "X's Turn"
    glutPostRedisplay()

def check_win():
    global gameOver, winner, message
    for r in range(GRID_SIZE):
        if board[r][0] != EMPTY and board[r][0] == board[r][1] == board[r][2]:
            winner = board[r][0]
            break
    if winner is None:
        for c in range(GRID_SIZE):
            if board[0][c] != EMPTY and board[0][c] == board[1][c] == board[2][c]:
                winner = board[0][c]
                break
    if winner is None:
        if board[0][0] != EMPTY and board[0][0] == board[1][1] == board[2][2]:
            winner = board[0][0]
        elif board[0][2] != EMPTY and board[0][2] == board[1][1] == board[2][0]:
            winner = board[0][2]

    if winner is not None:
        gameOver = True
        message = ("X Wins!" if winner == PLAYER_X else "O Wins!")
        return True
    return False

def check_draw():
    global gameOver, message
    if gameOver:
        return False
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == EMPTY:
                return False
    gameOver = True
    message = "It's a Draw!"
    return True

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    draw_grid()
    draw_pieces()
    draw_restart_button()
    draw_text(10, WINDOW_HEIGHT - 20, message)
    glutSwapBuffers()

def reshape(w, h):
    global WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE, button_rect
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, w, h, 0.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    WINDOW_WIDTH = w
    CELL_SIZE = w // GRID_SIZE
    WINDOW_HEIGHT = h
    button_rect = (w // 2 - 50, h - 60, 100, 40)

def mouse_click(button, state, x, y):
    global currentPlayer, message
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        bx, by, bw, bh = button_rect
        if bx <= x <= bx + bw and by <= y <= by + bh:
            reset_game()
            return

        if gameOver:
            return

        if y < GRID_SIZE * CELL_SIZE:
            col = x // CELL_SIZE
            row = y // CELL_SIZE

            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and board[row][col] == EMPTY:
                board[row][col] = currentPlayer
                if not check_win():
                    if not check_draw():
                        currentPlayer = PLAYER_O if currentPlayer == PLAYER_X else PLAYER_X
                        message = ("X's Turn" if currentPlayer == PLAYER_X else "O's Turn")
                glutPostRedisplay()

def init_gl():
    glClearColor(COLOR_BACKGROUND[0], COLOR_BACKGROUND[1], COLOR_BACKGROUND[2], 1.0)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Simple Tic Tac Toe")
    init_gl()
    reset_game()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse_click)
    glutMainLoop()

if __name__ == "__main__":
    main()