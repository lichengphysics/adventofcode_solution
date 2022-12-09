from helper import a_star

WAITING_COLS = [1, 2, 4, 6, 8, 10, 11]
ROOM_COLS = [3, 5, 7, 9]
FINAL_NODE = tuple()
COST = {"A": 1, "B": 10, "C": 100, "D": 1000}


def expand(node):
    waitings, rooms = node
    if all(all(x == letter for x in rooms[loc]) for loc, letter in zip(range(4), "ABCD")):
        return [(0, FINAL_NODE)]

    return room_to_waiting(node) + waiting_to_room(node)


def is_forbidden_path(waitings, waiting_loc, room_loc):
    c1, c2 = waiting_loc, room_loc
    if c1 > c2:
        c1, c2 = c2, c1
    return any(col in WAITING_COLS and waitings[WAITING_COLS.index(col)] != "" for col in range(c1 + 1, c2))


def room_to_waiting(node):
    waitings, rooms = node
    result = []
    for i, room in enumerate(rooms):
        if all(x == "" for x in room):
            continue
        room_loc = ROOM_COLS[i]

        room_idx = 0
        while room_idx < len(room):
            if room[room_idx] != "":
                break
            room_idx += 1
        to_move = room[room_idx]

        for j, waiting_loc in enumerate(WAITING_COLS):
            if waitings[j] != "":
                continue

            if is_forbidden_path(waitings, waiting_loc, room_loc):
                continue

            # have this person move over there
            distance = abs(waiting_loc - room_loc) + 1 + room_idx
            cost = distance * COST[to_move]

            new_waitings = list(waitings)
            new_rooms = [list(x) for x in rooms]
            new_waitings[j] = to_move
            new_rooms[i][room_idx] = ""
            result.append((cost, (tuple(new_waitings), tuple(map(tuple, new_rooms)))))
    return result


def waiting_to_room(node):
    waitings, rooms = node
    result = []
    for j, waiting_loc in enumerate(WAITING_COLS):
        to_move = waitings[j]
        if to_move == "":
            continue
        target_room_ord = ord(to_move) - ord('A')
        target_room = rooms[target_room_ord]

        room_loc = ROOM_COLS[target_room_ord]

        if target_room[0] != "":
            continue
        elif all(x == "" for x in target_room):
            room_idx = len(target_room) - 1
        else:
            room_idx = 0
            while room_idx < len(target_room):
                if target_room[room_idx] != "":
                    break
                room_idx = room_idx + 1
            if target_room[room_idx] != to_move:
                continue
            else:
                room_idx = room_idx - 1

        if is_forbidden_path(waitings, waiting_loc, room_loc):
            continue

        distance = abs(waiting_loc - room_loc) + 1 + room_idx
        cost = distance * COST[to_move]

        new_waitings = list(waitings)
        new_rooms = [list(x) for x in rooms]
        new_waitings[j] = ""
        new_rooms[target_room_ord][room_idx] = to_move

        result.append((cost, (tuple(new_waitings), tuple(map(tuple, new_rooms)))))
    return result


def solution(part1=True):
    with open("input.txt", "r") as f:
        input_data = f.read().split("\n")

    rooms = []
    for room_col in ROOM_COLS:
        rooms.append([input_data[row][room_col] for row in [2, 3]])
    if not part1:
        new_part2 = ["DD", "CB", "BA", "AC"]
        rooms = [[rooms[i][0], new_part2[i][0], new_part2[i][1], rooms[i][1]] for i in range(len(rooms))]

    rooms = tuple([tuple(x) for x in rooms])

    print(rooms)
    waitings = ("",) * 7

    out, path = a_star((waitings, rooms), expand, FINAL_NODE)
    for p in path:
        print(p)

    print("out:", out)


print("part 1: ")
solution()
print("part 2: ")
solution(False)
