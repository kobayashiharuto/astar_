import tracemalloc


def format_bytes(size):
    power = 2 ** 10  # 2**10 = 1024
    n = 0
    power_labels = ['B', 'KB', 'MB', 'GB', 'TB']
    while size > power and n <= len(power_labels):
        size /= power
        n += 1
    return 'current used memory: {:.3f} {}'.format(size, power_labels[n])


def log_memory():
    snapshot = tracemalloc.take_snapshot()
    size = sum([stat.size for stat in snapshot.statistics('filename')])
    print(format_bytes(size))
    return size
