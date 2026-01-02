from task_engine.cli.parser import parse_args
from task_engine.cli.runner import run
import sys

def main() -> None:
    try:
        args = parse_args()
        run(args)  # Running the workflow via cli through the run method.
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(0)

    sys.exit(0)

if __name__ == "__main__":
    main()