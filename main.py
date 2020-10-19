from sys import argv

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

directions = ['Up', 'Right', 'Down', 'Left']

dl = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]
matrix = [[int]]

end_states: [(int, int)] = list()


class InputOptions:
    GIVEN_INITIAL_AND_END_STATE: int = 0
    FIND_INITIAL_AND_END_STATE: int = 1
    FIND_INITIAL_AND_ALL_END_STATES: int = 2


def is_final_state(state: (int, int)) -> bool:
    global end_states
    global bkt_trace

    # print(bkt_trace)

    if end_states:
        return state in end_states

    matrix_len = len(matrix)
    matrix_wid = len(matrix[0])

    return matrix[state[0]][state[1]] == 0 and state[0] == 0 or state[1] == 0 or state[0] == matrix_len - 1 or \
           state[1] is matrix_wid - 1


def transition_state(state: (int, int), direction: directions) -> (int, int):
    if not is_transition_valid(state, direction):
        return state

    # direction_index = 0
    # for direct in directions:
    #     if direct == direction:
    #         break
    #     direction_index += 1

    direction_index = directions.index(direction)

    return state[0] + dl[direction_index], state[1] + dc[direction_index]


def is_transition_valid(state: (int, int), direction: directions) -> bool:
    direction_index = directions.index(direction)
    # for direct in directions:
    #     if direct == direction:
    #         break
    #     direction_index += 1

    future_state = (state[0] + dl[direction_index], state[1] + dc[direction_index])

    if future_state[0] < 0 or future_state[0] >= len(matrix) or future_state[1] < 0 or future_state[1] >= len(matrix[0]):
        return False

    return matrix[future_state[0]][future_state[1]] == 0


def init_func(maze_file_name: str = 'inputMaze.txt', option: int = InputOptions.GIVEN_INITIAL_AND_END_STATE) -> ([[int]], (int, int), [(int, int)]):
    try:
        with open(maze_file_name, 'r') as input_file:
            if option == InputOptions.GIVEN_INITIAL_AND_END_STATE:
                init_pos = input_file.readline().strip().split(',')
                init_pos_int = (int(init_pos[0]), int(init_pos[1]))
                end_pos = input_file.readline().strip().split(',')
                end_pos_int = (int(end_pos[0]), int(end_pos[1]))

            mat = list()
            line = 0

            for read_line in input_file.readlines():
                mat.append(list())
                for char in str(read_line):
                    if char == '0' or char == '1':
                        mat[line].append(int(char))
                line += 1

            # print(f'Initial state : {init_pos_int}')
            # for mat_line in mat:
            #     print(mat_line)

            if option == InputOptions.FIND_INITIAL_AND_END_STATE or option == InputOptions.FIND_INITIAL_AND_ALL_END_STATES:
                break_find = False
                for i in range(len(mat)):
                    if break_find:
                        break
                    for j in range(len(mat[i])):
                        if mat[i][j] == 0:
                            init_pos_int = (i, j)
                            break_find = True
                            break

            if option == InputOptions.FIND_INITIAL_AND_END_STATE:
                for i in range(1, len(mat)):
                    for j in range(1, len(mat[i])):
                        if mat[-i][-j] == 0:
                            return mat, init_pos_int, [(len(mat) - i, len(mat[0])-j)]

            if option == InputOptions.FIND_INITIAL_AND_ALL_END_STATES:
                end_states = []
                for i in range(len(mat)):
                    if mat[i][len(mat[i]) - 1] == 0:
                        end_states.append((i, len(mat[i]) - 1))

                for j in range(len(mat[0])):
                    if mat[len(mat) - 1][j] == 0:
                        end_states.append((len(mat)-1, j))

                return mat, init_pos_int, end_states

            return mat, init_pos_int, [end_pos_int]

    except IOError as file_error:
        print(f'N-am ce sa-ti fac : {file_error}')


class Algorithm:
    BFS = 0
    BACKTRACK = 1
    HILL_CLIMBING = 2
    BONUS = 3


bkt_trace: [[int]] = list()
stop_backtrack = False


def backtrack(state: (int, int)):
    global stop_backtrack
    global bkt_trace

    if is_final_state(state):
        bkt_trace[state[0]][state[1]] = 2
        stop_backtrack = True

    if not stop_backtrack:

        bkt_trace[state[0]][state[1]] = 2

        for direction in directions:
            if is_transition_valid(state, direction):
                backtrack(transition_state(state, direction))
                if stop_backtrack:
                    break

        if not stop_backtrack:
            bkt_trace[state[0]][state[1]] = 0


def hill_climb_bkt(state: (int, int)):
    global stop_backtrack
    global bkt_trace

    if is_final_state(state):
        bkt_trace[state[0]][state[1]] = 2
        stop_backtrack = True

    if not stop_backtrack:

        bkt_trace[state[0]][state[1]] = 2
        possible_states = []
        for direction in directions:
            if is_transition_valid(state, direction):
                possible_states.append(transition_state(state, direction))

        possible_states.sort(key=lambda x: x[0] + x[1], reverse=True)
        # print(possible_states)

        for state in possible_states:
            hill_climb_bkt(state)

            if stop_backtrack:
                break
        # backtrack(transition_state(state, direction))
        # if stop_backtrack:
        #     break

        if not stop_backtrack:
            bkt_trace[state[0]][state[1]] = 0


def backtrack_start(state: (int, int)) -> (bool, [[int]]):
    global bkt_trace
    global end_states
    bkt_trace = matrix.copy()

    backtrack(state)

    # print(bkt_trace)

    for end_state in end_states:
        if bkt_trace[end_state[0]][end_state[1]] > 1:
            return True, bkt_trace

    return False, bkt_trace


def hill_climb(state: (int, int)) -> (bool, [[int]]):
    global bkt_trace
    global end_states
    bkt_trace = matrix.copy()

    hill_climb_bkt(state)

    # print(bkt_trace)

    for end_state in end_states:
        if bkt_trace[end_state[0]][end_state[1]] > 1:
            return True, bkt_trace

    return False, bkt_trace


def bfs(state: (int, int)) -> (bool, [[int]]):
    global end_states
    global matrix
    # mat_copy = matrix.copy()
    queue = [state]

    while queue:
        current_state = queue[0]
        queue.remove(queue[0])
        for direction in directions:
            if is_transition_valid(current_state, direction):
                queue.append(transition_state(current_state, direction))
                matrix[queue[-1][0]][queue[-1][1]] = 2

    for end_state in end_states:
        if matrix[end_state[0]][end_state[1]] > 1:
            return True, matrix

    return False, matrix


def solve_labyrinth(mat: [[int]], initial_state: (int, int), algorithm_option: int = Algorithm.BACKTRACK):
    global matrix
    matrix = mat.copy()

    if algorithm_option == Algorithm.BACKTRACK:
        solution = backtrack_start( initial_state )
        print(solution[0])
        for line in solution[1]:
            print(line)

    if algorithm_option == Algorithm.BFS:
        solution = bfs(initial_state)
        print(solution[0])
        for line in solution[1]:
            print(line)

    if algorithm_option == Algorithm.HILL_CLIMBING:
        solution = hill_climb(initial_state)
        print(solution[0])
        for line in solution[1]:
            print(line)


def init_ai():
    if len(argv) < 2:
        print('py main.py -i inputMaze.txt [-o1 | -o2 | -o3]')
        exit(0)
        # option = InputOptions.FIND_INITIAL_AND_END_STATE

    file_name = None

    try:
        file_name = argv[argv.index('-i') + 1]
        print(file_name)
    except ValueError as NoInputGivenException:
        print('use -i <inputFile> to give maze input')
        exit(0)

    option = None

    try:
        argv.index('-o1')
        option = InputOptions.GIVEN_INITIAL_AND_END_STATE
    except ValueError as OptionOneNotSelected:
        pass

    try:
        argv.index('-o2')
        option = InputOptions.FIND_INITIAL_AND_END_STATE
    except ValueError as OptionTwoNotSelected:
        pass

    try:
        argv.index('-o3')
        option = InputOptions.FIND_INITIAL_AND_ALL_END_STATES
    except ValueError as OptionTwoNotSelected:
        pass

    if option is None:
        print('An option was not given. Expecting initial and end state in file')
        option = InputOptions.GIVEN_INITIAL_AND_END_STATE

    problem_data = init_func(file_name, option)

    global end_states
    end_states = problem_data[2].copy()

    # print(problem_data)
    solve_labyrinth(problem_data[0], problem_data[1], Algorithm.HILL_CLIMBING)


if __name__ == '__main__':
    init_ai()
