import argparse
import parameter
import user_interaction
import normalization.normalization as normalization
# ./cli.py --help
# ./cli.py --version
# ./cli.py --verbose

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

model_parser.add_argument('--create', action='store_true', help='Create model')
model_parser.add_argument('--describe', type=str, help='Describe model')
model_parser.add_argument('--edit-name', type=str, help='Edit model name')


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
    if args.describe:
        user_interaction.describe_model(args.describe)
    if args.edit_name:
        print("Edit name")
