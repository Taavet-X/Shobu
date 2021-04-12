inicial =  [
		[
			[2,2,2,2],
			[0,0,0,0],
			[0,0,0,0],
			[1,1,1,1],
		], [
			[2,2,2,2],
			[0,0,0,0],
			[0,0,0,0],
			[1,1,1,1],
		], [
			[2,2,2,2],
			[0,0,0,0],
			[0,0,0,0],
			[1,1,1,1],
		], [
			[2,2,2,2],
			[0,0,0,0],
			[0,0,0,0],
			[1,1,1,1],
		] ]

final =  [
		[
			[0,2,2,2],
			[0,0,0,0],
			[0,0,0,0],
			[1,1,1,1],
		], [
			[2,2,2,2],
			[0,0,0,0],
			[0,0,0,0],
			[1,1,1,0],
		], [
			[2,2,0,2],
			[0,0,0,0],
			[0,0,0,0],
			[1,1,1,1],
		], [
			[2,2,2,2],
			[0,0,0,0],
			[0,0,0,0],
			[1,1,1,1],
		] ]

def contador(boards):
    heuristica = 0
    player1 = 0
    player2 = 0
    for board in boards:
        for row in board:
            for value in row:
                if value == 1:
                    player1 += 1
                elif value == 2:
                    player2 +=1

    return player1, player2

def heuristica(inicial, current):
    p1i, p2i = contador(inicial)
    p1c, p2c = contador(current)

    heuristica = (p2i - p2c) - (p1i - p1c) 

    return heuristica

print(heuristica(inicial, final))