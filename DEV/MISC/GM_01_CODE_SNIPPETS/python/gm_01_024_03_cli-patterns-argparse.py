# PATTERN: CLI Patterns (argparse)

import argparse

def main():
    parser = argparse.ArgumentParser(description="Process some files.")
    # Arguments will be added here
    args = parser.parse_args()
    print("Parser initialized and arguments parsed.")

if __name__ == "__main__":
    main()

# PATTERN: CLI Patterns (argparse)

import argparse

def main():
    parser = argparse.ArgumentParser(description="Manage user data.")
    parser.add_argument('--user', type=str, required=True,
                        help='The username to operate on.')
    parser.add_argument('--id', type=int, default=0,
                        help='A unique identifier for the user.')
    args = parser.parse_args()
    print(f"Processing user: {args.user} with ID: {args.id}")

if __name__ == "__main__":
    main()

# PATTERN: CLI Patterns (argparse)

import argparse

def main():
    parser = argparse.ArgumentParser(description="Perform a simple calculation.")
    parser.add_argument('num1', type=float, help='The first number.')
    parser.add_argument('num2', type=float, help='The second number.')
    parser.add_argument('--operation', type=str, default='add',
                        choices=['add', 'subtract'], help='Operation to perform.')

    args = parser.parse_args()

    if args.operation == 'add':
        result = args.num1 + args.num2
    else:
        result = args.num1 - args.num2

    print(f"Result of {args.operation}ing {args.num1} and {args.num2}: {result}")

if __name__ == "__main__":
    main()

# PATTERN: CLI Patterns (argparse)

import argparse

def main():
    parser = argparse.ArgumentParser(description="Copy a file to a destination.")
    
    # Positional arguments
    parser.add_argument('source_path', type=str,
                        help='The path to the source file.')
    parser.add_argument('destination_path', type=str,
                        help='The path to the destination.')
    
    # Optional argument
    parser.add_argument('--force', '-f', action='store_true',
                        help='Overwrite destination if it exists.')
    
    args = parser.parse_args()
    
    print(f"Copying '{args.source_path}' to '{args.destination_path}'.")
    if args.force:
        print("Force overwrite enabled.")

if __name__ == "__main__":
    main()

# PATTERN: CLI Patterns (argparse)

import argparse

def main():
    parser = argparse.ArgumentParser(description="Run a script with optional debug mode.")
    
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose output.')
    parser.add_argument('--dry-run', action='store_true',
                        help='Perform a dry run without actual changes.')
    
    args = parser.parse_args()
    
    if args.verbose:
        print("Verbose mode enabled.")
    
    if args.dry_run:
        print("Performing a dry run...")
    else:
        print("Executing actual operations.")

if __name__ == "__main__":
    main()