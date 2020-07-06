def toCameCase(str):
    split = str.split("_")
    result = split[0]
    for s in split:
        if s == result:
            continue
        result += s.capitalize()
    return result


def firstUptoCameCase(str):
    split = str.split("_")
    result = split[0]
    for s in split:
        if s == result:
            continue
        result += s.capitalize()
    return result.capitalize()
