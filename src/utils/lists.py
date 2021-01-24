def list_map(pred, list_):
    return list(map(pred, list_))

def find_by(pred, list_):
    for item in list_:
        if pred(item):
            return item

    return None
