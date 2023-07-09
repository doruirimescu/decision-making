def create_type(t):
    print()
    print(f"Choose a {t.enum_name()}. The options are:")

    for e in t:
        print(f"{e.value}: {e.name}")
    n = ["", ""]
    while len(n) > 1:
        n = input(
            f"\nPlease enter the desired {t.enum_name()} number. \n"
            "If a description is needed, follow it by a zero:"
            ).split(" ")
        if len(n) > 1:
            print()
            print(t(int(n[0])).description)

    created_type = t(int(n[0]))
    print("You chose:", created_type.name)
    print()
    return created_type


def get_name(what: str):
    """Get the name of the model or parameter.
    """
    return input(f"Please, input the {what} name:")


def should_change_default(what: str, default_value) -> bool:
    answer = input(
            f"The default {what} is {default_value}. \n"
            "Would you like to change it ? (y/n)"
        )
    return answer == "y"

def get_range(what: str):
    r = input(
        f"Please, input the {what} range (min, max), "
        "or leave blank if there is no range: "
    ).split(",")
    return (float(r[0]), float(r[1])) if len(r) > 1 else None
