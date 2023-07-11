from ast import literal_eval
from typing import List

from colorama import Fore, Style

import dataset
import normalization.normalization as normalization
import parameter
from helpers import indent_n_chars, wrap_text_to_80_chars
from model import Model

# Constants for debugging
MODIFY_NORMALIZER = True
MODIFY_WEIGHT = True
CREATE_DATASET = True

##### MODEL BUILDING #####

def introduction():
    print(f"{Fore.GREEN}")
    print("Welcome to the decision making tool.")
    print("The decision making model consists of a few stages:")
    print("1. Model building stage. Here, you will define the model and its parameters.")
    print("2. Data collection stage. Here, you will collect data for the model.")
    print("3. Data analysis. Here, you will evaluate the model.")
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
        for k, v in additional_parameters.items():
            print(f"{k:15}: {v}")
        print()

    selected_parameter_values = {}
    if additional_parameters is not None:
        for k in additional_parameters.keys():
            answer = input(f"Please enter the value for {k}: ")
            if answer == "":
                answer = None
            else:
                answer = literal_eval(answer)
            selected_parameter_values[k] = answer

    print(selected_parameter_values)
    p = eval(f"parameter.{selected_parameter_name}(**{selected_parameter_values})")


    if MODIFY_NORMALIZER and should_change_default(
        "normalizer", p.normalizer.get_type()
        ):
        print()
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
    print()
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


def is_done() -> bool:
    r = input("Enter 'done' if you are done, or press enter to continue: ")
    print("")
    return r == "done"


def get_parameter_weights(parameters: List) -> None:
    print()
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
    print()


def create_dataset() -> dataset.Dataset:
    print("Would you like to create a new dataset or use an existing one?")
    print("0: Create a new dataset")
    print("1: Use an existing dataset")
    print("2: No")
    answer = input("Please enter the number of your choice: ")
    if answer == "0":
        dataset_name = input("Please enter the name of the dataset: ")
        dataset_description = input("Please enter a description of the dataset: ")

        d = dataset.Dataset(
            name=dataset_name,
            description=dataset_description,
        )
        d.store_json()
        return d
    elif answer == "1":
        answer = input("Please enter the name of the dataset: ")
        d = dataset.Dataset(**dataset.Dataset.load_json(answer))
        return d
    elif answer == "2":
        return None

def create_model() -> Model:
    introduction()
    name = get_name("model")
    print("Next, input the model parameters. When you are done, enter 'done'.")
    print("")
    should_continue = True
    parameters = []
    while should_continue:
        parameters.append(create_parameter())
        should_continue = not is_done()
    if MODIFY_WEIGHT:
        get_parameter_weights(parameters)

    should_continue = True
    datasets = []
    while should_continue:
        d = create_dataset()
        if d is not None:
            datasets.append(d)
        should_continue = not is_done()

    m = Model(name=name, parameters=parameters, datasets=datasets)
    print("You have created the following model: ", m)
    m.store_binary()
    return m


def list_class(t) -> None:
    for subclass in t.__subclasses__():
        name = subclass.__name__
        print(f"{name}:")
        DESCRIPTION = "  Description"
        initial_indent = 25 - len(DESCRIPTION)
        subsequent_indent = 25
        text = wrap_text_to_80_chars(
            subclass.get_description(),
            initial_indent,
            subsequent_indent)
        print(f'{DESCRIPTION}{text}')

        d = subclass.get_fields_and_their_description()
        if not d:
            print()
            continue
        fields="\n".join([f"{k} : {v}" for k,v in d.items()])
        FIELDS = "  Fields"
        initial_indent = 25 - len(FIELDS)
        print(f"{FIELDS}{wrap_text_to_80_chars(fields, initial_indent, subsequent_indent)}")
        print()


def describe_model(model_name: str) -> None:
    model = Model.load_binary(model_name)
    print(f"Name:")
    print(f"{indent_n_chars(model.name, 2)}")
    print()
    print("Parameters:")
    for p in model.parameters:
        print(f"  {p.__repr__()}")
        print()

    print("Datasets:")
    for d in model.datasets:
        print(f"  {d.__repr__()}")


def delete_model(model_name: str) -> None:
    Model.delete_binary(model_name)


def edit_model_name(model_name: str) -> None:
    model = Model.load_binary(model_name)
    new_name = get_name("new model")
    model.name = new_name
    model.store_binary()
    Model.delete_binary(model_name)
    print(f"The model {model_name} has been renamed to {new_name}.")


def delete_model_param(model_name: str, param_name: str) -> None:
    model = Model.load_binary(model_name)
    model.delete_parameter(param_name)
    model.store_binary()
    print(f"The parameter {param_name} has been deleted from {model_name}.")


def add_model_param(model_name: str) -> None:
    model = Model.load_binary(model_name)
    model.add_parameter(create_parameter())
    model.store_binary()
    print(f"The parameter has been added to {model_name}.")


def list_model_datasets(model_name: str) -> None:
    model = Model.load_binary(model_name)
    datasets = model.datasets
    if datasets:
        print(f"The datasets for {model_name} are:")
        for d in datasets:
            print(f"{d.__repr__()}")
    else:
        print(f"There are no datasets for {model_name}.")


def add_model_dataset(model_name: str) -> None:
    model = Model.load_binary(model_name)
    ds = create_dataset()
    model.add_dataset(ds)
    model.store_binary()


def delete_model_dataset(model_name: str, dataset_name: str) -> None:
    model = Model.load_binary(model_name)
    model.delete_dataset(dataset_name)
    model.store_binary()
    print(f"The dataset {dataset_name} has been deleted from {model_name}.")
