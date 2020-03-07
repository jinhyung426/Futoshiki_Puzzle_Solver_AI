#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = futoshiki_csp_model_1(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the Futoshiki puzzle.

1. futoshiki_csp_model_1 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only
      binary not-equal constraints for both the row and column constraints.

2. futoshiki_csp_model_2 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only n-ary
      all-different constraints for both the row and column constraints.

'''
from cspbase import *
import itertools


def futoshiki_csp_model_1(futo_grid):
    n = len(futo_grid)
    gen = itertools.takewhile(lambda key: key < n + 1, itertools.count(1, 1))
    lst_of_domain = list(gen)
    general_sat_tuple = list(itertools.permutations(range(1, n+1), 2))

    csp = CSP("Model_1")
    var_lst = []
    for i in range(n):
        var_lst.append([])

    constraint_lst = []

    for i in range(n):
        for j in range(n):
            var_lst[i].append(Variable(f'{i+1}th row {j+1}th column variable', []))

    for i in range(n):
        for j in range(2 * n - 1):
            if j % 2 == 0:
                if futo_grid[i][j] == 0:
                    var_lst[i][int(j/2)].add_domain_values(lst_of_domain)

                else:
                    var_lst[i][int(j/2)].add_domain_values([futo_grid[i][j]])
                    var_lst[i][int(j/2)].assign(futo_grid[i][j])

            else:
                constraint = Constraint(
                    f'{i + 1}th row {int(j/2) + 1}th column constraint',
                    [var_lst[i][int(j/2)], var_lst[i][int(j/2) + 1]])

                if futo_grid[i][j] == '.':
                    continue

                elif futo_grid[i][j] == '>':
                    # constraint.add_satisfying_tuples()
                    for t in general_sat_tuple:
                        if t[0] > t[1]:
                            constraint.add_satisfying_tuples([t])

                else:
                    # constraint.add_satisfying_tuples()
                    for t in general_sat_tuple:
                        if t[0] < t[1]:
                            constraint.add_satisfying_tuples([t])

                constraint_lst.append(constraint)


    number = 1

    for row in range(n):
        for num1 in range(n):
            for num2 in range(num1 + 1, n):
                if num1 != num2:
                    c = Constraint(f'Row constraint no.{number}',
                            [var_lst[row][num1], var_lst[row][num2]])
                    c.add_satisfying_tuples(general_sat_tuple)
                    constraint_lst.append(c)
                    number += 1

    number = 1

    for column_number in range(n):
        for num3 in range(n):
            for num4 in range(num3 + 1, n):
                if num3 != num4:
                    c = Constraint(f'Column constraint no.{number}',
                            [var_lst[num3][column_number], var_lst[num4][column_number]])
                    c.add_satisfying_tuples(general_sat_tuple)
                    constraint_lst.append(c)
                    number += 1

    for i in range(n):
        for j in range(n):
            csp.add_var(var_lst[i][j])

    for i in range(len(constraint_lst)):
        csp.add_constraint(constraint_lst[i])

    return csp, var_lst


def futoshiki_csp_model_2(futo_grid):
    n = len(futo_grid)
    gen = itertools.takewhile(lambda key: key < n + 1, itertools.count(1, 1))
    lst_of_domain = list(gen)
    general_sat_tuple_nary = list(itertools.permutations(range(1, n + 1), n))
    general_sat_tuple_binary = list(itertools.permutations(range(1, n+1), 2))

    csp = CSP("Model_2")
    var_lst = []
    for s in range(n):
        var_lst.append([])

    constraint_lst = []

    for i in range(n):
        for j in range(n):
            var_lst[i].append(Variable(f'{i+1}th row {j+1}th column variable', []))

    for i in range(n):
        for j in range(2 * n - 1):
            if j % 2 == 0:
                if futo_grid[i][j] == 0:
                    var_lst[i][int(j/2)].add_domain_values(lst_of_domain)

                else:
                    var_lst[i][int(j/2)].add_domain_values([futo_grid[i][j]])
                    var_lst[i][int(j/2)].assign(futo_grid[i][j])

            else:
                constraint = Constraint(
                    f'{i + 1}th row {int(j/2) + 1}th column constraint',
                    [var_lst[i][int(j/2)], var_lst[i][int(j/2) + 1]])

                if futo_grid[i][j] == '.':
                    continue
                elif futo_grid[i][j] == '>':
                    # constraint.add_satisfying_tuples()
                    for t in general_sat_tuple_binary:
                        if t[0] > t[1]:
                            constraint.add_satisfying_tuples([t])
                else:
                    # constraint.add_satisfying_tuples()
                    for t in general_sat_tuple_binary:
                        if t[0] < t[1]:
                            constraint.add_satisfying_tuples([t])

                constraint_lst.append(constraint)


    number = 1

    for row_number in range(n):
        # add row_constraint
        row_scope_lst = []
        for i in range(n):
            row_scope_lst.append(var_lst[row_number][i])

        c = Constraint(f'Row constraint no.{number}', row_scope_lst)
        c.add_satisfying_tuples(general_sat_tuple_nary)
        constraint_lst.append(c)
        number += 1

    number = 1

    for column_number in range(n):
        # add column_constraint
        column_scope_lst = []
        for i in range(n):
            column_scope_lst.append(var_lst[i][column_number])

        c = Constraint(f'Column constraint no.{number}', column_scope_lst)
        c.add_satisfying_tuples(general_sat_tuple_nary)
        constraint_lst.append(c)
        number += 1

    for i in range(n):
        for j in range(n):
            csp.add_var(var_lst[i][j])

    for i in range(len(constraint_lst)):
        csp.add_constraint(constraint_lst[i])

    return csp, var_lst

