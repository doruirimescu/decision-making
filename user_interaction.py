from typing import List, Tuple
from colorama import Fore, Style

def introduction():
    print(f"{Fore.GREEN}")
    print("Welcome to the decision making tool.")
    print("The decision making model consists of a few stages:")
    print("1. Model building stage. Here, you will define the model and its parameters.")
    print("2. Data collection stage. Here, you will collect data for the model.")
    print("3. Model evaluation stage. Here, you will evaluate the model.")
    print("4. Decision making stage. Here, you will make a decision based on the model.")
    print(f"{Style.RESET_ALL}")
    print("")

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
    return input(
        f"Please, input the {what} name: "
        )


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


def input_model_parameters():
    print("Next, input the model parameters. When you are done, enter 'done'.")
    print("")


def model_created(m):
    print("You have created the following model: ", m)


def is_done():
    r = input("Enter 'done' if you are done, or press enter to continue: ")
    print("")
    return r == "done"


def get_parameter_weights(parameters: List):
    print(
        "Next, we are going to define the weights for each parameter.\n"
        "Initially, all the parameters have the same weight (1).\n"
        "The weights are used to calculate the total score of a model.\n"
        "The higher the weight, the more important the parameter is.\n"
        "The total score of a model is the sum of the scores of its parameters.\n"
        )

    for i, p in enumerate(parameters):
        print(f"{i}: parameter: {p.name} weight: {p.weight}")

    def get_answer():
        return input("Enter the index of the parameter you want to change, or enter 'done': ")
    answer = get_answer()
    while answer != "done":
        answer = get_answer()
        i = int(answer)
        w = input("Enter the new weight: ")
        parameters[i].weight = float(w)
        print(f"Parameter {i} has weight {w}.")


    print("The new parameters are:")

    for i, p in enumerate(parameters):
        print(f"{i}: parameter: {p.name} weight: {p.weight}")
