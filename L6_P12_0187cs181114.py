'L6_P12_0187cs181114'
import math
initial_pos = [0, 0]
final_pos = [0, 0]
k = int(input())
for i in range(0, k):
    move = input().split(' ')
    dire = move[0]
    mag = int(move[1])
    if dire == 'UP':
        final_pos[0] = final_pos[0]+mag
    elif dire == 'DOWN':
        final_pos[0] = final_pos[0] - mag
    elif dire == 'LEFT':
        final_pos[1] = final_pos[1] - mag
    elif dire == 'RIGHT':
        final_pos[1] = final_pos[1] + mag
distance = math.sqrt(final_pos[0]**2 + final_pos[1]**2)
print(round(distance))
