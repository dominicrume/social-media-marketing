import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Say hello to someone.")
    parser.add_argument("--name", type=str, required=True, help="The name to greet")
    
    args = parser.parse_args()
    
    try:
        print(f"Hello, {args.name}! The system is improving everyday.")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
