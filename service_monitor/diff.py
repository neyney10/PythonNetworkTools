

def difflist(lst1,lst2):
    A = set(lst1)
    B = set(lst2)
    diff = A.symmetric_difference(B)

    return diff

        
