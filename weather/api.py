def tmaccess():
    api = open("access.txt")
    access = api.read()
    api.close()
    return access
