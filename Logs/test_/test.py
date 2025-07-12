import curses
import glob
import time
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass

from configs import crud_test_configs, drf_test_configs
from utils.crud_endpoint_unittest import EndpointCRUDUnitTesting
from utils.drf_api_unittesting import DRFAPIUnitTesting
from utils.manual_unittesting import ManualEndpointUnitTesting


def get_manual_test_json_list() -> list:
    """
    load all json file in [manual_test_json] dir

    Returns:
        list: list of json files
    """
    return glob.glob('manual_test_json\\*.json')


@dataclass
class MenuOption:
    """Represents a menu option with title and associated data."""
    title: str
    option: str
    action: Optional[Callable[[str], None]] = None
    next_menu: Optional[int] = None


@dataclass
class Menu:
    """Represents a menu with a title and list of options."""
    title: str
    options: List[MenuOption]


class EndpointTester:
    def __init__(self, stdscr):
        self.menu_status = True
        self.stdscr = stdscr
        self.setup_curses()
        self.current_menu = 0
        self.selected_option = 0
        self.results = []
        self.menus = self.define_menus()
        self.selected_result: dict = {}

    def setup_curses(self) -> None:
        """Initialize curses settings."""
        curses.curs_set(0)  # Hide cursor
        self.stdscr.timeout(100)  # Set input timeout
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Highlight color
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Title color
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Welcome color

    def define_menus(self) -> List[Menu]:
        """Define all menus and their options."""
        return [
            Menu(
                title="Main Menu",
                options=[
                    MenuOption("Manual Testing", "manual", next_menu=1),
                    MenuOption("CRUD Testing", "crud", action=self.run_crud_test),
                    MenuOption("DRF-Swagger Testing", "drf-swagger", action=self.run_drf_swagger_test),
                    MenuOption("Exit", "exit", action=self.exit_program)
                ]
            ),
            Menu(
                title="Manual Testing Options",
                options=[
                    MenuOption("All", "all", action=self.run_all_manual_tests),
                ]+[
                    MenuOption(json_path.split('\\')[-1], json_path, action=self.run_manual_test) for json_path in get_manual_test_json_list()
                ]+[
                    MenuOption("Back", "back", next_menu=0)
                ]
            )
        ]

    def display_welcome(self) -> None:
        """Display a styled welcome message."""
        self.stdscr.clear()
        welcome_lines = [
            "****************************************",
            "* Welcome to Endpoint Tester!           *",
            "* Test your APIs with ease and style!  *",
            "****************************************"
        ]
        for i, line in enumerate(welcome_lines):
            self.stdscr.addstr(i + 1, 2, line, curses.color_pair(3) | curses.A_BOLD)
        self.stdscr.addstr(len(welcome_lines) + 2, 2, "Press any key to continue...", curses.A_DIM)
        self.stdscr.refresh()
        self.stdscr.getch()

    def display_menu(self) -> None:
        """Display the current menu."""
        self.stdscr.clear()
        menu = self.menus[self.current_menu]

        # Display title with border
        title = f" {menu.title} "
        self.stdscr.addstr(0, 0, "*" * (len(title) + 4), curses.color_pair(2))
        self.stdscr.addstr(1, 2, title, curses.color_pair(2) | curses.A_BOLD)
        self.stdscr.addstr(2, 0, "*" * (len(title) + 4), curses.color_pair(2))

        # Display options
        for idx, option in enumerate(menu.options):
            y = idx + 4
            display_text = f"> {option.title}" if idx == self.selected_option else f"  {option.title}"
            if idx == self.selected_option:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, 2, display_text)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, 2, display_text)

        # Display footer
        self.stdscr.addstr(len(menu.options) + 5, 2, "Use ↑↓ to navigate, Enter to select", curses.A_DIM)
        self.stdscr.refresh()

    def run_manual_test(self, option: str) -> None:
        """Execute a manual test for the given endpoint."""
        self.results.append(f"Running manual test for {option}")
        self.display_result(f"Manual Test: {option} executed successfully!")

        self.selected_result: dict = {
            'option': 'manual_test',
            'selected': option
        }
        self.exit_program('')

    def run_all_manual_tests(self, option: str) -> None:
        """Execute all manual tests."""
        self.results.append("Running all manual tests")
        self.display_result("All Manual Tests executed successfully!")

        self.selected_result: dict = {
            'option': 'manual_test',
            'selected': 'all'
        }
        self.exit_program('')

    def run_crud_test(self, option: str) -> None:
        """Execute CRUD testing."""
        self.results.append("Running CRUD test")
        self.display_result("CRUD Test executed successfully!")

        self.selected_result: dict = {
            'option': 'crud',
        }
        self.exit_program('')

    def run_drf_swagger_test(self, option: str) -> None:
        """Execute DRF-Swagger testing."""
        self.results.append("Running DRF-Swagger test")
        self.display_result("DRF-Swagger Test executed successfully!")

        self.selected_result: dict = {
            'option': 'drf-swagger',
        }
        self.exit_program('')

        # drf_test = DRFAPIUnitTesting(**drf_test_configs)
        # drf_test.run_test()

    def exit_program(self, option: str) -> None:
        """Exit the program and display results."""
        self.stdscr.clear()
        self.stdscr.addstr(0, 2, "Test Results:", curses.color_pair(2) | curses.A_BOLD)
        for i, result in enumerate(self.results):
            self.stdscr.addstr(i + 2, 2, result)
        self.stdscr.addstr(len(self.results) + 3, 2, "Thank you for using Endpoint Tester!", curses.color_pair(3))
        self.stdscr.addstr(len(self.results) + 4, 2, "Press any key to exit...", curses.A_DIM)
        self.stdscr.refresh()
        self.stdscr.getch()
        self.menu_status = False

    def display_result(self, message: str) -> None:
        """Display a result message temporarily."""
        self.stdscr.clear()
        self.stdscr.addstr(2, 2, message, curses.color_pair(3) | curses.A_BOLD)
        self.stdscr.addstr(4, 2, "Press any key to continue...", curses.A_DIM)
        self.stdscr.refresh()
        self.stdscr.getch()

    def run(self) -> dict:
        """Main program loop."""
        self.display_welcome()
        while self.menu_status:
            self.display_menu()
            try:
                key = self.stdscr.getch()
            except:
                continue

            menu = self.menus[self.current_menu]
            if key == curses.KEY_UP and self.selected_option > 0:
                self.selected_option -= 1
            elif key == curses.KEY_DOWN and self.selected_option < len(menu.options) - 1:
                self.selected_option += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                option = menu.options[self.selected_option]
                if option.action:
                    option.action(option.option)
                if option.next_menu is not None:
                    self.current_menu = option.next_menu
                    self.selected_option = 0

        return self.selected_result


def main(stdscr):
    tester = EndpointTester(stdscr)
    return tester.run()


if __name__ == "__main__":
    selected_option = curses.wrapper(main)

    match selected_option['option']:

        case 'crud':

            crud_test = EndpointCRUDUnitTesting(**crud_test_configs)
            crud_test.run_test()

        case 'drf-swagger':

            drf_test = DRFAPIUnitTesting(**drf_test_configs)
            drf_test.run_test()

        case 'manual_test':

            if selected_option['selected'] == 'all':

                for json_path in get_manual_test_json_list():
                    print(f'\n\nRun Test [{json_path.split('\n\n')[0]}]:')
                    manual_testing = ManualEndpointUnitTesting(endpoint_json_path=json_path)
                    manual_testing.run_test()

            else:

                manual_testing = ManualEndpointUnitTesting(endpoint_json_path=selected_option['selected'])
                manual_testing.run_test()
