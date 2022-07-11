import pygame, copy, time

screen_width, screen_height = 500, 500

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE|pygame.DOUBLEBUF|pygame.SCALED)
pygame.display.set_caption('Conway Game Of Life')

square = []
square_copy = []

die = False
pressed = False
draw_mode = True
width = 50
delay_time = 2

def detectNeighbours(scan_x, scan_y):
    neighbour = 0

    eight_directions = [
        [scan_x + 1, scan_y],
        [scan_x - 1, scan_y],
        [scan_x + 1, scan_y + 1],
        [scan_x + 1, scan_y - 1],
        [scan_x - 1, scan_y + 1],
        [scan_x - 1, scan_y - 1],
        [scan_x, scan_y + 1],
        [scan_x, scan_y - 1],
        ]

    for direction in eight_directions:
        if direction[0] < 0 or direction[1] < 0:
            continue

        if direction in square:
            neighbour += 1
    
    return neighbour

while not die:
    screen.fill([10, 10, 10])

    x = pygame.mouse.get_pos()[0] // width 
    y = pygame.mouse.get_pos()[1] // width 

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            die = True 

        if ev.type == pygame.MOUSEBUTTONDOWN and draw_mode:
            if [x, y] not in square:
                square.append([x, y])
            else:
                square.remove([x, y]) # HOW COULD I HAVE FORGOT ABOUT .REMOVE WHEN I WAS DOING THIS. IT TOOK ME 5 MINS TO GOOGLE.

        if ev.type == pygame.WINDOWLEAVE:
            x = y = 0

        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
            draw_mode = False if draw_mode else True

        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_UP:
            delay_time += 1

        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_DOWN:
            delay_time -= 1 if delay_time - 0.1 > 0 else 0

    if not draw_mode:
        square_copy = []
        for item in square:
            scan_x, scan_y = item[0], item[1]

            eight_directions = [
                [scan_x + 1, scan_y],
                [scan_x - 1, scan_y],
                [scan_x + 1, scan_y + 1],
                [scan_x + 1, scan_y - 1],
                [scan_x - 1, scan_y + 1],
                [scan_x - 1, scan_y - 1],
                [scan_x, scan_y + 1],
                [scan_x, scan_y - 1],
                ]

            for direction in eight_directions:
                if direction not in square:
                    if direction[0] < 0 or direction[1] < 0:
                        continue

                    if detectNeighbours(direction[0], direction[1]) == 3 and direction not in square_copy:
                        square_copy.append(direction)

            alive_neighbours = detectNeighbours(scan_x, scan_y)

            if alive_neighbours in [2, 3] and len([x for x in item if x > 0 and x < screen_width // width]) == 2:
                square_copy.append(item)

        square = copy.deepcopy(square_copy)
        time.sleep(delay_time // 10)

    for item in square:
        pygame.draw.rect(screen, [255, 255, 255], pygame.Rect(item[0]*width, item[1]*width, width, width))

    print("Time delay:", delay_time)

    pygame.display.flip()
