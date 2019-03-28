

# diffset is a function which returns the differences between two sets, returns two sets as well,
# each one have all the elements not found in the other.
# Input: set1,set2 as two sets.
# Output: a list contains two sets.
def diffset(set1,set2):
    A = set1 # old services
    B = set2 # new services

    started_services = B - A
    closed_services = A - B

    return [started_services,closed_services]


        
