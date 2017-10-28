assignments = []
from utils import *
cols='123456789'
rows='ABCDEFGHI'
def cross(A, B):

    "Cross product of elements in A and elements in B."
    return [j+i for j in A for i in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
#Just add the diagonal_units to the unitlist so that it gets added to the constrints when checked for the "1-9"numbers
diagonal_units = [[x+y for x, y in zip(rows, cols)], [x+y for x, y in zip(rows, cols[::-1])]]

unitlist = row_units + column_units + square_units+ diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        for box in unit:
            if(len(values[box])==2):
            #    print("box with 2 vals:"+box)
                for box_peer in unit:
                    if (values[box] == values[box_peer])&(box!=box_peer)&(len(values[box_peer])==2):
                        #print("matching box with 2 vals:"+box)
                    #    print("box,peer"+box+" "+box_peer)
                        for box_peer_replace in unit:
                            for i in values[box]:
                                if (i in values[box_peer_replace]) & (values[box_peer_replace]!=values[box])&(len(values[box_peer_replace])!=1):
                        #            print("replacing place"+box_peer_replace)
                            #        print("matching digit"+i)
                            #        print("valuematched"+values[box])
                                    #values[box_peer_replace]=values[box_peer_replace].replace(i,"")
                                    values = assign_value(values, box_peer_replace, values[box_peer_replace].replace(i,''))
                            #        display(values)
                            #        print("-------44444----------")


    return values
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """


    grid_dict = dict(zip(boxes,grid))
    for i,j in grid_dict.items():
        if j=='.':
            grid_dict[i]='123456789'
    return grid_dict

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """

    if values == False:
        print("No Solution found")
    else:
        width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            #values[peer] = values[peer].replace(digit,'')
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values

def only_choice(values):
    for units in square_units:
        #For each square units
        for digit in '123456789':
            dplaces=[]
            for unit in units:
                #each cell of one square unit
                #Check if one number occurs at only one place
                if (digit) in values[unit]:
                    dplaces.append(unit)
                #print(dplaces)
            if len(dplaces)==1:
                #   values[dplaces[0]]=digit
                new_values = assign_value(values, dplaces[0], digit)

    return new_values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):

    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku=values.copy()
        #new_sudoku[s]=value
        new_sudoku = assign_value(new_sudoku, s, value)

        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values=grid_values(grid)

    solved_sudoku=search(values)

    if solved_sudoku:
        return solved_sudoku
    else:
        return False


if __name__ == '__main__':
    test='9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    solved=solve(test)
    display(solved)
    #display(grid_values(diag_sudoku_grid))
    assignments.append(solved.copy())

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
