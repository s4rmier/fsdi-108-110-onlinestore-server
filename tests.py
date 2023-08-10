from config import me


def read():
    print(me["name"])

    if "height" in me:
        print(me["height"])


def modify():
    me["age"] = 98
    print(me)


def create():
    me["preferred_color"] = "blue"
    print(me)


def remove():
    me["hobbies"].pop()
    print(me)


read()
modify()
create()
remove()
