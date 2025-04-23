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


def Greedy(head, tail, fruits, grid, C):
    head_x = head.x
    head_y = head.y
    fruit = fruits[0]
    fruit_x = fruit.x
    fruit_y = fruit.y
    dist = 9999
    best_action = []
    best_action_head = None
    size = 0
    temp_best_action = []
    #temp_dist = 9999
    if head_y+1 < 10 and grid[head_y+1, head_x] != "🟥":
        new_dist = distance((head_y+1, head.x), (fruit_y, fruit_x))
        new_head = Point(head.x, head_y+1)
        bfs = bfs_check(new_head, grid, tail, fruits, C)
        bfs_size = bfs[1]
        if  new_dist < dist and bfs[0]:
            best_action.clear()
            action_head = new_head
            dist = new_dist
            action = 'down'
            best_action.append((action_head, action))
        elif new_dist == dist and bfs[0]:
            action_head = new_head
            dist = new_dist
            action = 'down'
            best_action.append((action_head, action))
        if bfs_size > size:
            temp_best_action.clear()
            size = bfs_size
            temp_action_head = new_head
            #temp_dist = new_dist
            temp_action = 'down'
            temp_best_action.append((temp_action_head, temp_action))
            
        elif bfs_size == size:
            size = bfs_size
            temp_action_head = new_head
            #temp_dist = new_dist
            temp_action = 'down'
            temp_best_action.append((temp_action_head, temp_action))



    if head_x+1 < 10 and  grid[head_y, head_x+1] != "🟥":
        new_dist = distance((head_y, head.x+1), (fruit_y, fruit_x))
        new_head = Point(head.x+1, head_y)
        bfs = bfs_check(new_head, grid, tail, fruits, C)
        bfs_size = bfs[1]

        if  new_dist < dist and bfs[0]:
            best_action.clear()
            action_head = new_head
            dist = new_dist
            action = 'right'
            best_action.append((action_head, action))
        elif  new_dist == dist and bfs[0]:
            action_head = new_head
            dist = new_dist
            action = 'right'
            best_action.append((action_head, action))  
        if bfs_size > size:
            temp_best_action.clear()
            size = bfs_size
            temp_action_head = new_head
            #temp_dist = new_dist
            temp_action = 'right'
            temp_best_action.append((temp_action_head, temp_action))

        elif bfs_size == size:
            size = bfs_size
            temp_action_head = new_head
            #temp_dist = new_dist
            temp_action = 'right'
            temp_best_action.append((temp_action_head, temp_action))

    if head_y-1 >= 0 and grid[head_y-1, head_x] != "🟥":
        new_dist = distance((head_y-1, head.x), (fruit_y, fruit_x))
        new_head = Point(head.x, head_y-1)
        bfs = bfs_check(new_head, grid, tail, fruits, C)
        bfs_size = bfs[1]
        if  new_dist < dist and bfs[0]:
            best_action.clear()
            action_head = new_head
            dist = new_dist
            action = 'up'
            best_action.append((action_head, action))
        if  new_dist == dist and bfs[0]:
            action_head = new_head
            dist = new_dist
            action = 'up'
            best_action.append((action_head, action))  
        if bfs_size > size:
            temp_best_action.clear()
            size = bfs_size
            temp_action_head = new_head
            #temp_dist = new_dist
            temp_action = 'up'
            temp_best_action.append((temp_action_head, temp_action))
        elif bfs_size == size:
            size = bfs_size
            temp_action_head = new_head
            #temp_dist = new_dist
            temp_action = 'up'
            temp_best_action.append((temp_action_head, temp_action))

    if head_x-1 >= 0 and grid[head_y, head_x-1] != "🟥":
        new_dist = distance((head_y, head.x-1), (fruit_y, fruit_x))
        new_head = Point(head.x-1,head_y)
        bfs = bfs_check(new_head, grid, tail, fruits, C)
        bfs_size = bfs[1]
        if  new_dist < dist and bfs[0]:
            best_action.clear()
            action_head = new_head
            dist = new_dist
            action = 'left'
            best_action.append((action_head, action))
        elif  new_dist == dist and bfs[0]:
            action_head = new_head
            dist = new_dist
            action = 'left'
            best_action.append((action_head, action))  
        if bfs_size > size:
            temp_best_action.clear()
            size = bfs_size
            temp_action_head = new_head
            #temp_dist = new_dist
            temp_action = 'left' 
            temp_best_action.append((temp_action_head, temp_action))
        if bfs_size == size:
            size = bfs_size
            temp_action_head = new_head
            #temp_dist = new_dist
            temp_action = 'left' 
            temp_best_action.append((temp_action_head, temp_action))

    if len(best_action) == 0:
        #return ()
        if len(temp_best_action) == 0:
            return None, head, tail, best_action
        temp = random.choice(temp_best_action)
        action_head = temp[0]
        best_action = temp[1]
        #dist = temp_dist
    else:
        temp = random.choice(best_action)
        action_head = temp[0]
        best_action = temp[1]
 
    # print(grid)
    # print(f"Current head: {head}")
    # print(f"New head: {new_head}")
    # print(f"Tail: {tail}")
    # print(f"Best action: {best_action}")
    
    return action_head, head, tail, best_action

   
    # for loc in locations:
    #     for fruit in fruits:
    #         distance = manhattan_distance(loc, fruit)
    #         if distance < min_distance:
    #             min_distance = distance
    #             best_action = loc
    
    # return best_action

def bfs_check(new_head, grid, tail, fruits, C):
    #print(f"grid before: \n{grid}")
    head_x = new_head.x
    head_y = new_head.y
    last = tail[-1]
    original = grid[new_head.y, new_head.x]
    #print(f"Original: {original}")

    grid[new_head.y, new_head.x] = "💀"
    if original == "⬜":
        grid[last.y, last.x] = "⬜"
        num_of_whites = 100 - len(tail) - 1
    if original == "🍏":
        num_of_whites = 100 - len(tail) - 2
    #print(f"num_of_whites: {num_of_whites}")
    
    #print(f"grid in between: \n{grid}")
    visited = []
    queue = []
    if 0 <= head_y+1 < 10 and (grid[head_y+1, head_x] in ("⬜", "🍏")):
        queue.append((head_y+1, head_x))
        visited.append((head_y+1, head_x))
    elif 0 <= head_y-1 < 10 and (grid[head_y-1, head_x] in ("⬜", "🍏")):
        queue.append((head_y-1, head_x))
        visited.append((head_y-1, head_x))
    elif 0 <= head_x+1 < 10 and (grid[head_y, head_x+1] in ("⬜", "🍏")):
        queue.append((head_y, head_x+1))
        visited.append((head_y, head_x+1))
    elif 0 <= head_x-1 < 10 and (grid[head_y, head_x-1] in ("⬜", "🍏")):
        queue.append((head_y, head_x-1))
        visited.append((head_y, head_x-1))
    while len(queue) != 0:
        queue, visited = bfs(grid, visited, queue)
    #print(f"len visited: {len(visited)}")
    if len(visited) >= num_of_whites*C:
        grid[new_head.y, new_head.x] = original
        grid[last.y, last.x] = "🟥"
        #print(f"grid after: \n{grid}")
        #print("true")
        return (True, len(visited))
    else:
        max = 0
        if 0 <= head_y+1 < 10 and (grid[head_y+1, head_x] in ("⬜", "🍏")):
            visited = []
            queue = []
            queue.append((head_y+1, head_x))
            visited.append((head_y+1, head_x))
            while len(queue) != 0:
                queue, visited = bfs(grid, visited, queue)
            temp = len(visited)
            if temp > max:
                max = temp
        elif 0 <= head_y-1 < 10 and (grid[head_y-1, head_x] in ("⬜", "🍏")):
            visited = []
            queue = []
            queue.append((head_y-1, head_x))
            visited.append((head_y-1, head_x))
            while len(queue) != 0:
                queue, visited = bfs(grid, visited, queue)
            temp = len(visited)
            if temp > max:
                max = temp
        elif 0 <= head_x+1 < 10 and (grid[head_y, head_x+1] in ("⬜", "🍏")):
            visited = []
            queue = []
            queue.append((head_y, head_x+1))
            visited.append((head_y, head_x+1))
            while len(queue) != 0:
                queue, visited = bfs(grid, visited, queue)
            temp = len(visited)
            if temp > max:
                max = temp
        elif 0 <= head_x-1 < 10 and (grid[head_y, head_x-1] in ("⬜", "🍏")):
            visited = []
            queue = []
            queue.append((head_y, head_x-1))
            visited.append((head_y, head_x-1))
            while len(queue) != 0:
                queue, visited = bfs(grid, visited, queue)
            temp = len(visited)
            if temp > max:
                max = temp
        grid[new_head.y, new_head.x] = original
        grid[last.y, last.x] = "🟥"
        #print(f"grid after: \n{grid}") 
        #print("false")
        return (False, max)

def bfs(grid, visited, queue):
    first = queue.pop(0)
    #print(f"first: {first}")
    first_x = first[1]
    first_y = first[0]
    if first_y+1 < 10 and grid[first_y+1, first_x] in ("⬜", "🍏")  and (first_y+1, first_x) not in visited:
        queue.append((first_y+1, first_x))
        visited.append((first_y+1, first_x))
    if first_y-1 >= 0 and grid[first_y-1, first_x] in ("⬜", "🍏") and (first_y-1, first_x) not in visited:
        queue.append((first_y-1, first_x))
        visited.append((first_y-1, first_x))
    if first_x+1 < 10 and grid[first_y, first_x+1] in ("⬜", "🍏") and (first_y, first_x+1) not in visited:
        queue.append((first_y, first_x+1))
        visited.append((first_y, first_x+1))
    if first_x-1 >= 0 and grid[first_y, first_x-1] in ("⬜", "🍏") and (first_y, first_x-1) not in visited:
        queue.append((first_y, first_x-1))
        visited.append((first_y, first_x-1))
    #print(f"queue: {queue}")
    #print(f"visited: {visited}")
    return queue, visited



def move(grid, tail, new_head, old_head, score, fruits):
    last = tail[-1]
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

def run_greedy(head, tail, fruits, grid, C):
    score = 0
    #while True:
    for i in range(5000):
        new_head, old_head, tail, best_action = Greedy(head, tail, fruits, grid, C)
        print(best_action)
        if new_head is None:
            #print("GG")
            #print(f"Score: {score}")
            return score
        new_grid, tail, score, fruits = move(grid, tail, new_head, old_head, score, fruits)
        print(grid)
        print(f"Score: {score}")
        grid = new_grid
        head = new_head
        time.sleep(0.1)  # Wait 0.3 seconds before next step
        #print(grid)
    #return grid, tail

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

head = Point(7,6)
tail = [Point(8,6), Point(9,6)]
fruits = [Point(4,6)]
grid = plot(head, tail, fruits) 
#Greedy(head, tail, fruits, grid)
#constants = [i/10 for i in range(10, 11)]
A = 0


x = 1
C = 1
#output_file_aug = "V3.txt"
#with open(output_file_aug, "w") as f:
total_score = 0
for i in range(x):
    head = Point(7,6)
    tail = [Point(8,6)]
    fruits = [Point(6,6)]
    grid = plot(head, tail, fruits) 
    score = run_greedy(head, tail, fruits, grid, C)
    print(i)
    print(f"Score: {score}")
    # f.write(f"{score}\n")
    # f.flush()
    total_score += score
average_score = total_score / x
print(f"Average score: {C, average_score}")