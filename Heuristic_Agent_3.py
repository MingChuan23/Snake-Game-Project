import numpy as np
from snake_game import Point
import random
import time
#take in snake locations and fruit
first_perspective = {
     0: 'stay',
     1: 'left',
     2: 'right'
 }

third_perspective = {
           0: 'up',
           1: 'down',
           2: 'left',
           3: 'right'
}

def Greedy(head, tail, fruits, grid, score):
    head_x = head.x
    head_y = head.y
    fruit = fruits[0]
    fruit_x = fruit.x
    fruit_y = fruit.y
    dist = 9999
    best_action = []
    action_head = None
    possible_action = []
    #temp_dist = 9999
    if head_y+1 < 10 and grid[head_y+1, head_x] != "🟥":
        new_dist = distance((head_y+1, head.x), (fruit_y, fruit_x))
        new_head = Point(head.x, head_y+1)
        bfs = bfs_check(new_head, grid, tail, fruits, score)
        action = 'down'
        possible_action.append((new_head, action))
        
        if  new_dist < dist and bfs and side_check(head, grid, tail, fruits, score):
            best_action.clear()
            action_head = new_head
            dist = new_dist
            
            best_action.append((action_head, action))
        elif new_dist == dist and bfs:
            action_head = new_head
            dist = new_dist
            best_action.append((action_head, action))

    if head_x+1 < 10 and  grid[head_y, head_x+1] != "🟥":
        new_dist = distance((head_y, head.x+1), (fruit_y, fruit_x))
        new_head = Point(head.x+1, head_y)
        bfs = bfs_check(new_head, grid, tail, fruits, score)
        action = 'right'
        possible_action.append((new_head, action))
        if  new_dist < dist and bfs and side_check(head, grid, tail, fruits, score):
            best_action.clear()
            action_head = new_head
            dist = new_dist
            
            best_action.append((action_head, action))
        elif  new_dist == dist and bfs:
            action_head = new_head
            dist = new_dist
            best_action.append((action_head, action))  
        

    if head_y-1 >= 0 and grid[head_y-1, head_x] != "🟥":
        new_dist = distance((head_y-1, head.x), (fruit_y, fruit_x))
        new_head = Point(head.x, head_y-1)
        bfs = bfs_check(new_head, grid, tail, fruits, score)
        action = 'up'
        possible_action.append((new_head, action))
        
        if  new_dist < dist and bfs and side_check(head, grid, tail, fruits, score):
            best_action.clear()
            action_head = new_head
            dist = new_dist
            best_action.append((action_head, action))
        if  new_dist == dist and bfs:
            action_head = new_head
            dist = new_dist
            best_action.append((action_head, action))  


    if head_x-1 >= 0 and grid[head_y, head_x-1] != "🟥":
        new_dist = distance((head_y, head.x-1), (fruit_y, fruit_x))
        new_head = Point(head.x-1,head_y)
        bfs = bfs_check(new_head, grid, tail, fruits, score)
        action = 'left'
        possible_action.append((new_head, action))
        
        if  new_dist < dist and bfs and side_check(head, grid, tail, fruits, score):
            best_action.clear()
            action_head = new_head
            dist = new_dist

            best_action.append((action_head, action))
        elif  new_dist == dist and bfs:
            action_head = new_head
            dist = new_dist
            best_action.append((action_head, action))  
            


    if len(best_action) == 0:
        if len(possible_action) == 0:
            return None, head, tail, best_action
        temp = random.choice(possible_action)
        action_head = temp[0]
        best_action = temp[1]
    else:
        temp = random.choice(best_action)
        action_head = temp[0]
        best_action = temp[1]

 
    # print(grid)
    # print(f"Current head: {head}")
    # print(f"New head: {new_head}")
    # print(f"Tail: {tail}")
    # print(f"Best action: {best_action}")
    if best_action == "up":
        return 0
    elif best_action == "down":
        return 1
    elif best_action == "left":
        return 2
    elif best_action == "right":
        return 3
    return best_action

   
    # for loc in locations:
    #     for fruit in fruits:
    #         distance = manhattan_distance(loc, fruit)
    #         if distance < min_distance:
    #             min_distance = distance
    #             best_action = loc
    
    # return best_action
def side_check(head, grid, tail, fruits, score):
    around = []
    around2 = []
    last = tail[0]
    head_x = head.x
    head_y = head.y
    fruit_x = fruits[0].x
    fruit_y = fruits[0].y
    for i in range(-1, 2):
        for j in range(-1, 2):
            if head_x+i < 10 and head_x+i >= 0 and head_y+j < 10 and head_y+j >= 0:
                temp = (head_y+j, head_x+i)
                around.append(temp)
                #around.append(temp2)
    for i in range(-1, 2):
        for j in range(-1, 2):
            if fruit_x+i < 10 and fruit_x+i >= 0 and fruit_y+j < 10 and fruit_y+j >= 0:
                #print(f"fruit_x: {fruit_x+i}, fruit_y: {fruit_y+j}")
                temp2 = (fruit_y+j, fruit_x+i)
                around2.append(temp2)
    #print(around2)
    count = 0
    count2 = 0
    for i in around2:
        #print(i)
        if grid[i[0], i[1]] == "⬜":
            count += 1
    for i in around:
        if grid[i[0], i[1]] == "⬜":
            count2 += 1
    if ((last.y, last.x) in around and (fruits[0].y, fruits[0].x) in around) and ((last.y, last.x) in around and (head.y, head.x) in around) and count == 0 and count2 == 0 and score > 10:
        return False
    # if (last.y, last.x) in around and (head.y, head.x) in around and score > 10:
    #     return False
    # if (last.y, last.x) in around and (fruits[0].y, fruits[0].x) in around and score > 10:
    #     return False
    return True

def bfs_check(new_head, grid, tail, fruits, score):
    #print(f"grid before: \n{grid}")
    head_x = new_head.x
    head_y = new_head.y
    last = tail[0]
    visited = []
    queue = []
    original = grid[new_head.y, new_head.x]
    #print(f"Original: {original}")
    grid[head_y, head_x] = "💀"
    if original == "⬜":
        grid[last.y, last.x] = "⬜"
        num_of_whites = 100 - len(tail) - 1
    if original == "🍏":
        grid[last.y, last.x] = "🟦"
        #queue.append((last.y, last.x))
        #num_of_whites = 100 - len(tail) - 2
    # grid[last.y, last.x] = "⬜"
    # num_of_whites = 100 - len(tail) - 1
    #print(f"num_of_whites: {num_of_whites}")
    #print(f"grid in between: \n{grid}")
    
    if 0 <= head_y+1 < 10 and (grid[head_y+1, head_x] in ("⬜", "🍏")):
        queue.append((head_y+1, head_x))
        visited.append((head_y+1, head_x))
    if 0 <= head_y-1 < 10 and (grid[head_y-1, head_x] in ("⬜", "🍏")):
        queue.append((head_y-1, head_x))
        visited.append((head_y-1, head_x))
    if 0 <= head_x+1 < 10 and (grid[head_y, head_x+1] in ("⬜", "🍏")):
        queue.append((head_y, head_x+1))
        visited.append((head_y, head_x+1))
    if 0 <= head_x-1 < 10 and (grid[head_y, head_x-1] in ("⬜", "🍏")):
        queue.append((head_y, head_x-1))
        visited.append((head_y, head_x-1))

    while len(queue) != 0 and last not in queue:
        queue, visited = bfs(grid, visited, queue, last)
    #print(f"queue: {queue}")
    #print(f"visited: {visited}")
    #print(f"len visited: {len(visited)-1}")
    
    # around = []
    # for i in range(-1, 2):
    #     for j in range(-1, 2):
    #         if last.x+i < 10 and last.x+i >= 0 and last.y+j < 10 and last.y+j >= 0:
    #             temp = (last.y+j, last.x+i)
    #             around.append(temp)
    # count = 0
    # for i in around:
    #     if grid[i[0], i[1]] == "⬜":
    #         count += 1




    if last in queue or score < 0:
        grid[new_head.y, new_head.x] = original 
        grid[last.y, last.x] = "🟥"
        #print(f"grid after: \n{grid}")
        #print("true")
        return True
    else:
        grid[new_head.y, new_head.x] = original
        grid[last.y, last.x] = "🟥"
        #print(f"grid after: \n{grid}") 
        #print("false")
        #return ()
        return False

def bfs(grid, visited, queue, last):
    first = queue.pop(0)
    #print(f"first: {first}")
    first_x = first[1]
    first_y = first[0]
    if last.y == first_y and last.x == first_x:
        queue.clear()
        queue.append(last)
        return queue, visited
    if first_y+1 < 10 and grid[first_y+1, first_x] in ("⬜", "🍏", "🟦")  and (first_y+1, first_x) not in visited:
        queue.append((first_y+1, first_x))
        visited.append((first_y+1, first_x))
    if first_y-1 >= 0 and grid[first_y-1, first_x] in ("⬜", "🍏", "🟦") and (first_y-1, first_x) not in visited:
        queue.append((first_y-1, first_x))
        visited.append((first_y-1, first_x))
    if first_x+1 < 10 and grid[first_y, first_x+1] in ("⬜", "🍏", "🟦") and (first_y, first_x+1) not in visited:
        queue.append((first_y, first_x+1))
        visited.append((first_y, first_x+1))
    if first_x-1 >= 0 and grid[first_y, first_x-1] in ("⬜", "🍏", "🟦") and (first_y, first_x-1) not in visited:
        queue.append((first_y, first_x-1))
        visited.append((first_y, first_x-1))
    return queue, visited


def move(grid, tail, new_head, old_head, score, fruits):
    last = tail[0]
    #print(last)
    if grid[new_head.y, new_head.x] == "🍏":
        score += 1
        grid[new_head.y, new_head.x] = "💀"
        grid[old_head.y, old_head.x] = "🟥"
        tail.insert(0, old_head)
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        while grid[y, x] != "⬜":
            x = random.randint(0, 9)
            y = random.randint(0, 9)
        fruits = [Point(x, y)]
        grid[y, x] = "🍏"
    else:
        grid[new_head.y, new_head.x] = "💀"
        grid[old_head.y, old_head.x] = "🟥"
        grid[last.y, last.x] = "⬜"
        tail.insert(0, old_head)
        tail.pop(-1)

    # print(f"New head: {new_head}")
    # print(f"Old head: {old_head}")
    # print(f"Tail: {tail}")
    return grid, tail, score, fruits



def distance(point1, point2):
    #print(abs(point1[0] - point2[0]) + abs(point1[1] - point2[1]))
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def plot(head, tail, fruits):
    grid = np.full((10, 10), '⬜', dtype='U1')
    #print(grid)
    for tail in tail:
        grid[tail.y, tail.x] = "🟥"  # Mark snake locations with 1
    grid[head.y, head.x] = "💀"  # Mark snake head with 1
    for fruit in fruits:
        grid[fruit.y, fruit.x] = "🍏"  # Mark fruit locations with 2
    #print(grid)
    return grid
def run_greedy_tail(head, tail, fruits, grid):
    score = 0
    moves = 0
    #while True:
    best_action = Greedy(head, tail, fruits, grid, score)
    print(best_action)
    # if new_head is None:
    #     print("GG")
    #     print(f"Score: {score}")
    #     return score
    # if score == 97:
    #     print("completed")
    #     print(f"Score: {score}")
    #     return score
    # if moves > 3000:
    #     print("Exceeded")
    #     print(f"Score: {score}")
    #     return score
    #new_grid, tail, score, fruits = move(grid, tail, new_head, old_head, score, fruits)
    #moves += 1
    #print(grid)
    #print(f"Score: {score}")
    #grid = new_grid
    #head = new_head
    #time.sleep(0.0)  # Wait 0.3 seconds before next step
    #print(grid)
    
    return best_action
# head = Point(7,6)
# tail = [Point(8,6), Point(9,6)]
# fruits = [Point(4,6)]
# grid = plot(head, tail, fruits) 
# #Greedy(head, tail, fruits, grid)


# total_score = 0
# x = 10
# completed = 0
# for i in range(x):
#     head = Point(7,6)
#     tail = [Point(8,6)]
#     fruits = [Point(6,6)]
#     grid = plot(head, tail, fruits) 
#     print(i)
#     score = run_greedy(head, tail, fruits, grid)
#     # if score > 90 or score < 80:
#     #     break
#     if score == 97:
#         completed += 1
#         total_score += score
#         continue
#     total_score += score

# average_score = total_score / x
# print(f"Average score: {average_score}")
# print(f"Completed: {completed}")