#!venv/bin/python3

def cleanString(name):
    """Normalize scholarship name by getting rid of special characters
    like line feed, zero width space, ...

    Args:
        name (string): original scholarship name directly from html

    Returns:
        string: Clean name
    """
    NON_BREAK_SPACE_CHAR = u'\xa0'
    LF_CHAR = u'\n'  # line feed
    EOL_CHAR = u'\r\n'  # end of line
    ZERO_WIDTH_SPACE = u'\u200b'

    name = (name.strip()
            .replace(EOL_CHAR, ' ')
            .replace(NON_BREAK_SPACE_CHAR, ' ')
            .replace(ZERO_WIDTH_SPACE, '')
            .replace(LF_CHAR, '')
            )
    return name.strip()
    # return name.strip().split(' ')


if __name__ == "__main__":
    test = ['\u200bSTATE', 'OF', 'MAURITIUS',
            'POSTGRADUATE', 'SCHOLARSHIP', 'SCHEME', '2022/2023']
    print(cleanString(' '.join(test)))
