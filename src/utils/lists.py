def list_map(pred, list_):
    """
    Like the regular `map` but returns a list
    """
    return list(map(pred, list_))

def find_by(pred, list_):
    """
    Find element in a list by some predicate
    """
    for item in list_:
        if pred(item):
            return item

    return None
