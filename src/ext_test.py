import os

while True:

    path = input('path:')

    # split dir/file
    dir = os.path.dirname(path)
    base = os.path.basename(path)

    # split file name by dot
    file_array = base.split('.')

    # if there is at least one dot
    if len(file_array) > 1:

        # the result is the pre-dot plus first dot
        base = file_array[0] + '.' + file_array[-1]

    print(os.path.join(dir, base))
