from pathlib import Path

if __name__ == "__main__":
    old_path = Path(
        "/home/dana/Documents/Projects/Python/CLI_Test/dist/cli_test_1-2-3/assets/src/cli_test.py"
    )

    if old_path.exists():
        print("found old_path")

    new_path = Path(
        "/home/dana/Documents/Projects/Python/CLI_Test/dist/cli_test_1-2-3/assets/src/cli_test"
    )

    old_path.rename(new_path)
