def road_length(island):
    rows = len(island)
    cols = len(island[0])
    roads = 0
    for row in range(0, rows):
        for col in range(0, cols):
            # print (rows, cols)
            print("Currently on ", row, col, island[row][col])
            if island[row][col] == 'W':
                continue
                # print(row, col, "is a W")
            else:
                # print(row, col, "is a I")
                if (col-1 < 0):
                    roads += 1
                    continue
                if col+1 > cols-1:
                    roads += 1
                    continue
                if (row-1 < 0):
                    roads += 1
                    continue
                if row+1 > rows-1:
                    roads += 1
                    continue
                if island[row-1][col] == 'W':
                    roads += 1
                if island[row+1][col] == 'W':
                    roads += 1
                if island[row][col-1] == 'W':
                    roads += 1
                if island[row][col+1] == 'W':
                    roads += 1

    return f'We need {roads} roads.'


lambda_island = [['W', 'W', 'W', 'W'],
                 ['W', 'I', 'I', 'I'],
                 ['W', 'W', 'W', 'I']]

print('\n'.join(' '.join(map(str, sl)) for sl in lambda_island))
print(road_length(lambda_island))
