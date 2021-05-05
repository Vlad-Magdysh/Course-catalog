
def dict_factory(cursor, row):
    """
    Format sqlite row to dictionary
    :param cursor: cursor for the connection to sqlite database
    :param row: sqlite row
    :return: Dictionary representation of a row
    """
    items = {}
    for idx, col in enumerate(cursor.description):
        items[col[0]] = row[idx]
    return items
