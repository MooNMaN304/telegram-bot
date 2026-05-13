from src.application.value import get_malibu_controller
from src.application.admin_commands import run_parsing


def main():
    controller = get_malibu_controller()
    msg = run_parsing(controller)
    print(msg)


if __name__ == "__main__":
    main()
