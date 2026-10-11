from design import main as generate_assets
from generate_stats import generate as generate_stats, load_snapshot
from generate_terminal import main as generate_terminal


def main() -> None:
    generate_assets()
    generate_terminal()
    generate_stats(load_snapshot())


if __name__ == "__main__":
    main()
