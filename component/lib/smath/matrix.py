def matrix_rotate(matrix):
    new_matrix = {}

    for row_id in sorted(matrix.keys()):
        row = matrix[row_id]
        for col_id in sorted(row.keys()):
            v = row[col_id]
            if not col_id in new_matrix.keys():
                new_matrix[col_id] = {}
            #print "SET ROW %d COL %d => %s" % (col_id,row_id,v) 
            new_matrix[col_id][row_id] = v
    return new_matrix