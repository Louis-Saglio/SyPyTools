from collections import OrderedDict
from libifidi import sizeof_fmt

import psutil


def get_process_by_memory_size():
    return OrderedDict([(proc.pid, (proc.memory_info().rss, proc.exe(), proc.cpu_percent(), proc.name())) for proc in sorted(psutil.process_iter(), key=lambda x:x.memory_info().rss, reverse=True)])


def main():
    for name, (memory, cmd, cpu, name) in get_process_by_memory_size().items():
        if cmd:
            print(sizeof_fmt(memory).ljust(9), str(cpu) + ' %', name[:30].ljust(29),  cmd, sep='\t\t')


if __name__ == '__main__':
    main()
