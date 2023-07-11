import argparse
import parameter
import user_interaction
import normalization.normalization as normalization

parser = argparse.ArgumentParser(description='Decision making cli.')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--verbose', action='store_true', help='verbose output')

# Create subparsers
subparsers = parser.add_subparsers(dest='command')

# Create parser for "parameters" command
parameters_parser = subparsers.add_parser('parameters', help='Parameters related commands')
parameters_parser.add_argument('--list', action='store_true', help='List parameters and their descriptions')

# Create parser for "normalizers" command
parameters_parser = subparsers.add_parser('normalizers', help='Parameters related commands')
parameters_parser.add_argument('--list', action='store_true', help='List parameters and their descriptions')

# Create parser for "model" command
model_parser = subparsers.add_parser('model', help='Model related commands')
model_subparsers = model_parser.add_subparsers(dest='model_command')

model_parser.add_argument('--name', type=str, help='Select model')
model_parser.add_argument('--describe', action='store_true', help='Describe selected model')
model_parser.add_argument('--rename', action='store_true', help='Change selected model name')
model_parser.add_argument('--delete-param', type=str, help='Delete selected model parameters')
model_parser.add_argument('--add-param', action='store_true', help='Add a new parameter to the selected model')

model_parser.add_argument('--create', action='store_true', help='Create model')
model_parser.add_argument('--delete', action='store_true', help='Delete model')

model_parser.add_argument('--add-dataset', action='store_true', help='Add dataset to model')
model_parser.add_argument('--list-datasets', action='store_true', help='List datasets in model')

# Parse the command-line arguments
args = parser.parse_args()

# Perform actions based on the parsed command
if args.command == 'parameters':
    if args.list:
        user_interaction.list_class(parameter.Parameter)
elif args.command == 'normalizers':
    if args.list:
        user_interaction.list_class(normalization.Normalizer)
elif args.command == 'model':
    if args.create:
        user_interaction.create_model()
    elif args.name:
        selected_model = args.name
        if args.describe:
            user_interaction.describe_model(selected_model)
        elif args.rename:
            user_interaction.edit_model_name(selected_model)
        elif args.delete_param:
            param_to_delete = args.delete_param
            user_interaction.delete_model_param(selected_model, param_to_delete)
        elif args.add_param:
            user_interaction.add_model_param(selected_model)
        elif args.delete:
            user_interaction.delete_model(selected_model)
        elif args.add_dataset:
            user_interaction.add_model_dataset(selected_model)
        elif args.list_datasets:
            user_interaction.list_model_datasets(selected_model)
