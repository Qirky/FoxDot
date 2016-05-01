def LCM(*args):
    """ Lowest Common Multiple """
    # Base case
    if len(args) == 1: return args[0]

    X = list(args)
    
    while any([X[0]!=K for K in X]):

        i = X.index(min(X))
        X[i] += args[i]        

    return X[0]
