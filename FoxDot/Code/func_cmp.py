"""
    compare_functions.py(funcA, funcB):

        returns True if the functions are identical
    
"""

def func_cmp(funcA, funcB):

    codeA = funcA.__code__
    A_bytecode  = codeA.co_code
    A_constants = codeA.co_consts
    A_variables = codeA.co_names

    codeB = funcB.__code__
    B_bytecode  = codeB.co_code
    B_constants = codeB.co_consts
    B_variables = codeB.co_names
    
    return all([A_bytecode == B_bytecode,
                A_constants == B_constants,
                A_variables == B_variables])
