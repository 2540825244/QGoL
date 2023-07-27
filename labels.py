# label generator
def label_cell(x, y, t):
    return f"x{x}y{y}t{t}"

def label_same_as_next_time(x, y, t):
    return f"x{x}y{y}t{t}snt"

def label_more_than_3_neighbours(x, y, t):
    return f"x{x}y{y}t{t}m3"

def label_less_than_2_neighbours(x, y, t):
    return f"x{x}y{y}t{t}l2"

def label_2_neighbours(x, y, t):
    return f"x{x}y{y}t{t}e2"

def label_2_neighbours_helper_a(x, y, t):
    return f"x{x}y{y}t{t}e2a"

def label_2_neighbours_helper_b(x, y, t):
    return f"x{x}y{y}t{t}e2b"

def label_3_neighbours(x, y, t):
    return f"x{x}y{y}t{t}e3"

def label_3_neighbours_helper_a(x, y, t):
    return f"x{x}y{y}t{t}e3a"

def label_3_neighbours_helper_b(x, y, t):
    return f"x{x}y{y}t{t}e3b"