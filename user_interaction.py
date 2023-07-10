from typing import List, Tuple
from colorama import Fore, Style
import normalization.normalization as normalization
import parameter

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


def create_parameter():
    print()
    print(f"Choose a parameter. The options are:")

    for i, n in enumerate(parameter.Parameter.get_subclasses_as_list()):
        print(f"{i}: {n}")
    n = ["", ""]

    while len(n) > 1:
        n = input(
            f"\nPlease enter the desired parameter number. \n"
            "If a description is needed, follow it by a zero:"
            ).split(" ")
        selected_parameter_name = parameter.Parameter.get_subclasses_as_list()[int(n[0])]
        if len(n) > 1:
            print()
            description = eval(f"parameter.{selected_parameter_name}.get_description()")
            print(description)
            print()
    additional_parameters = eval(f"parameter.{selected_parameter_name}.get_fields_and_their_description()")
    if additional_parameters is not None:
        print()
        print("This parameter has the following parameters:")
        print()
        for k, v in additional_parameters.items():
            print(f"{k:15}: {v}")
        print()

    selected_parameter_values = {}
    if additional_parameters is not None:
        for k in additional_parameters.keys():
            from ast import literal_eval
            answer = input(f"Please enter the value for {k}: ")
            if answer == "":
                answer = None
            else:
                answer = literal_eval(answer)
            selected_parameter_values[k] = answer

    print(selected_parameter_values)
    p = eval(f"parameter.{selected_parameter_name}(**{selected_parameter_values})")


    if should_change_default(
        "normalizer", p.normalizer.get_type()
        ):
        p.normalizer = create_normalizer()
    return p

def create_normalizer():
    print()
    print("Choose a normalizer. The options are:")
    for i, n in enumerate(normalization.Normalizer.get_subclasses_as_list()):
        print(f"{i}: {n}")
    n = ["", ""]
    while len(n) > 1:
        n = input(
            f"\nPlease enter the desired normalizer number. \n"
            "If a description is needed, follow it by a zero:"
            ).split(" ")
        selected_normalizer_name = normalization.Normalizer.get_subclasses_as_list()[int(n[0])]
        if len(n) > 1:
            print()
            description = eval(f"normalization.{selected_normalizer_name}.get_description()")
            print(description)
            print()

    additional_parameters = eval(f"normalization.{selected_normalizer_name}.get_fields_and_their_description()")
    if additional_parameters is not None:
        print("This normalizer has additional parameters:")
        for k, v in additional_parameters.items():
            print(f"{k}: {v}")
        print()

    selected_parameter_values = {}
    if additional_parameters is not None:
        for k in additional_parameters.keys():
            selected_parameter_values[k] = input(f"Please enter the value for {k}: ")

    normalizer = eval(f"normalization.{selected_normalizer_name}(**{selected_parameter_values})")
    print(f"You created: {selected_normalizer_name}({selected_parameter_values})")
    print()
    return normalizer


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
