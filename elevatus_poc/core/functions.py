
def skip_limit(page_size, page_num):
    skips = int(page_size * (page_num - 1))
    return skips, page_size
