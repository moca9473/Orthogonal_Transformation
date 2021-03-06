def orthogonal_transformation(data):
    col_list = data.columns.tolist()
    if 'Date' in col_list:
        x = data[data.columns.difference(['Date'])]
        col_list.remove('Date')
    else:
        x = data
    x = x[col_list]

    K = len(x.columns)
    T = len(x)
    var_cov = x.cov()
    M = (T - 1) * var_cov

    # editing
    # inv = np.linalg.inv(M)
    # sqrtm = pd.DataFrame(linalg.sqrtm(inv))
    eigenvalue, eigenvector = np.linalg.eig(M)

    O = pd.DataFrame(eigenvector)
    D = pd.DataFrame(np.diag(eigenvalue))

    diag_values = pd.Series(np.diag(D))
    diag_values = 1 / np.sqrt(diag_values)
    D_minus_half = pd.DataFrame(0.00, index=np.arange(K), columns=np.arange(K))
    mat = D_minus_half.values
    mat[range(K), range(K)] = diag_values
    D_minus_half = pd.DataFrame(mat)
    O_trans = O.T

    # Calculating S and S_final
    S = np.matmul(np.matmul(O, D_minus_half), O_trans)
    S = pd.DataFrame(S)
    sigma = x.std()
    S_final = np.matmul(S, np.sqrt(T - 1) * np.diag(sigma))
    S_final = pd.DataFrame(S_final)

    # Calculating F_bar_orth
    x_mean = x.mean()
    F_arrow = x - x_mean
    F_arrow_orth = pd.DataFrame(np.matmul(F_arrow, S_final))  # (4)
    vector_ones = pd.DataFrame(1, index=range(T), columns=range(1))
    F_bar = pd.DataFrame(x_mean).T

    other_part = np.matmul(vector_ones, F_bar)
    other_part_2 = np.matmul(other_part, S_final)
    F_orth = F_arrow_orth + other_part_2
    F_orth.columns = x.columns
    F_orth = F_orth[x.columns]
    F_orth.index = x.index

    return F_orth