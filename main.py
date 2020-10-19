# input : labirint n x m,
#         pStart : xs, ys
#         pDest  : xd, yd

#         miscari : up down left right
#         misc. posibil de la un 0 la un 0

# stare =  unde mat[i][j] e o poz. in mat
#         (i, j)(i, j) poz in labirint
#         mat[i][j], in lab la poz i,j putem avea 0 : liber, 1 : zid, 2 : vizitat

# state = (i, j)
# dest = (i,j)

directions = ['Up', 'Down', 'Left', 'Right']

dl = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]
matrix = [[int]]


def is_final_state(state: (int, int)) -> bool:
    matrix_len = len(matrix)
    matrix_wid = len(matrix[0])

    return matrix[state[0]][state[1]] == 0 and state[0] == 0 or state[1] == 0 or state[0] == matrix_len - 1 or \
           state[1] is matrix_wid - 1


def transition_state(state: (int, int), direction: directions) -> (int, int):
    if not is_transition_valid(state, direction):
        return state

    direction_index = 0
    for direct in directions:
        if direct == direction:
            break
        direction_index += 1

    return state[0] + dl[direction_index], state[1] + dc[direction_index]


def is_transition_valid(state: (int, int), direction: directions) -> bool:
    direction_index = 0
    for direct in directions:
        if direct == direction:
            break
        direction_index += 1

    future_state = (state[0] + dl[direction_index], state[1] + dc[direction_index])

    if state[0] < 0 or state[0] >= len(matrix) or state[1] < 0 or state[1] < len(matrix[0]):
        return False

    return matrix[future_state[0]][future_state[1]] != 0


def init_func() -> ((int, int), [[int]]):
    try:
        with open('inputMaze.txt', 'r') as input_file:
            init_pos = input_file.readline().strip().split(',')
            init_pos_int = (int(init_pos[0]), int(init_pos[1]))

            mat = list()
            line = 0

            for read_line in input_file.readlines():
                mat.append(list())
                for char in str(read_line):
                    if char == '0' or char == '1':
                        mat[line].append(int(char))
                line += 1

            print(f'Initial state : {init_pos_int}')
            for mat_line in mat:
                print(mat_line)

            return init_pos_int, mat

    except IOError as file_error:
        print(f'N-am ce sa-ti fac : {file_error}')


if __name__ == '__main__':
    init_func()
