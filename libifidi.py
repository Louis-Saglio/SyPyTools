import os
from collections import OrderedDict


def sizeof_fmt(num, suffix='o'):
    """Readable file size
    :param num: Bytes value
    :type num: int
    :param suffix: Unit suffix (optionnal) default = o
    :type suffix: str
    :rtype: str
    """
    # Copy/pasted from SO
    for unit in ['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def get_file_size(path, log=False):
    try:
        return os.path.getsize(path)
    except (FileNotFoundError, PermissionError, BaseException) as e:
        if log:
            print(path, e)
        return 0


def libifidi(root):
    tree = {}
    all_files = list(os.walk(root))
    file_nbr = len(all_files)
    for i, (directory, _, files) in enumerate(all_files):
        i += 1
        pct = int(i * 100 / file_nbr)
        print('[' + (pct * '>').ljust(100, ' ') + ']', pct, '%', end='\r')
        tree[directory] = sum([get_file_size(os.path.join(directory, file)) for file in files])
    return OrderedDict([(file, tree[file]) for file in sorted(tree, key=lambda x: tree[x], reverse=True)])


def main(root, output_file, size_min):
    with open(output_file, 'w') as f:
        for file, size in libifidi(root).items():
            if size >= int(size_min):
                f.write(sizeof_fmt(size).ljust(12, ' ') + file + '\n')


if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
