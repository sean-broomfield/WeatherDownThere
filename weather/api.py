def tmaccess():
    api = open("access.txt")
    access = api.read()
    api.close()
    return access


def owaccess():
    api = open("owaccess.txt")
    access = api.read()
    api.close()
    return access
