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

def Greedy(head, tail, fruits, grid):
    head_x = head.x
    head_y = head.y
    fruit = fruits[0]
    fruit_x = fruit.x
    fruit_y = fruit.y
    dist = 9999
    best_action = ""
    action_head = None
    if head_y+1 < 10 and grid[head_y+1, head_x] != "🟥":
        new_dist = distance((head_y+1, head.x), (fruit_y, fruit_x))
        new_head = Point(head.x, head_y+1)
        if  new_dist < dist:
            action_head = new_head
            dist = new_dist
            best_action = 'down'



    if head_x+1 < 10 and  grid[head_y, head_x+1] != "🟥":
        new_dist = distance((head_y, head.x+1), (fruit_y, fruit_x))
        new_head = Point(head.x+1, head_y)

        if  new_dist < dist:
            action_head = new_head
            dist = new_dist
            best_action = 'right'


    if head_y-1 >= 0 and grid[head_y-1, head_x] != "🟥":
        new_dist = distance((head_y-1, head.x), (fruit_y, fruit_x))
        new_head = Point(head.x, head_y-1)
        if  new_dist < dist:
            action_head = new_head
            dist = new_dist
            best_action = 'up'

    if head_x-1 >= 0 and grid[head_y, head_x-1] != "🟥":
        new_dist = distance((head_y, head.x-1), (fruit_y, fruit_x))
        new_head = Point(head.x-1,head_y)

        if  new_dist < dist:
            action_head = new_head
            dist = new_dist
            best_action = 'left'

 
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
def run_greedy(head, tail, fruits, grid):
    score = 0
    #while True:
    for i in range(5000):
        new_head, old_head, tail, best_action = Greedy(head, tail, fruits, grid)
        #print(best_action)
        if new_head is None:
            #print("GG")
            #print(f"Score: {score}")
            return score
        new_grid, tail, score, fruits = move(grid, tail, new_head, old_head, score, fruits)
        #print(grid)
        #print(f"Score: {score}")
        grid = new_grid
        head = new_head
        time.sleep(0.0)  # Wait 0.3 seconds before next step
        #print(grid)
    #return grid, tail
head = Point(7,6)
tail = [Point(8,6)]
fruits = [Point(6,6)]
grid = plot(head, tail, fruits) 
#Greedy(head, tail, fruits, grid)

total_score = 0
x = 1000
output_file_aug = "V1.txt"
with open(output_file_aug, "w") as f:

    for i in range(x):
        head = Point(7,6)
        tail = [Point(8,6)]
        fruits = [Point(6,6)]
        grid = plot(head, tail, fruits) 
        print(i)
        score = run_greedy(head, tail, fruits, grid)
        print(f"Score: {score}")
        f.write(f"{score}\n")
        f.flush()
        total_score += score
average_score = total_score / x
print(f"Average score: {average_score}")