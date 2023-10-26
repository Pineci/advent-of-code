def get_dir(structure, path):
    current = structure
    for sub_dir in path:
        current = current[sub_dir]
    return current

def calculate_directory_size(structure: dict, prefix=""):
    sizes = {}
    current_size = 0
    for name, val in structure.items():
        if isinstance(val, dict):
            new_prefix = prefix+"/"+name
            dir_size, new_sizes = calculate_directory_size(val, new_prefix)
            sizes.update(new_sizes)
            sizes[new_prefix[1:]] = dir_size
            current_size += dir_size
        else:
            current_size += val
    return current_size, sizes

with open("input.txt", "rb") as file:
    structure = {"/": {}}
    current = []
    for line in file:
        line = line[:-1].decode("utf-8")
        if line[0] == "$":
            line = line[2:]
            args = line.split(" ")
            match args[0]:
                case "cd":
                    if args[1] == "..":
                        current = current[:-1]
                    else:
                        current.append(args[1])
                case "ls":
                    pass
        else:
            tokens = line.split(" ")
            if tokens[0] == "dir":
                get_dir(structure, current)[tokens[1]] = {}
            else:
                get_dir(structure, current)[tokens[1]] = int(tokens[0])

_, dir_sizes = calculate_directory_size(structure)
total_space = 70000000
needed_free_space = 30000000
current_free_space = total_space - dir_sizes["/"]
min_needed_size = needed_free_space-current_free_space
min_dir, min_size = None, None
for dir, size in dir_sizes.items():
    if size >= min_needed_size:
        if not min_size or size < min_size:
            min_dir, min_size = dir, size
print(min_size)