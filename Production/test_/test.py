import curses
import glob
from typing import List, Optional, Callable, Dict

from dataclasses import dataclass

from configs import crud_test_configs, drf_test_configs
from utils.crud_endpoint_unittest import EndpointCRUDUnitTesting
from utils.drf_api_unittesting import DRFAPIUnitTesting
from utils.manual_unittesting import ManualEndpointUnitTesting


def get_manual_test_json_list() -> List[str]:
    """
    Load all JSON files from the 'manual_test_json' directory.

    Returns:
        List[str]: List of file paths for JSON test files.
    """
    return glob.glob('manual_test_json\\*.json')


@dataclass
class MenuOption:
    """
    Represents a single menu option.

    Attributes:
        title (str): Display text for the menu option.
        option (str): Identifier or value associated with the option.
        action (Optional[Callable[[str], None]]): Function to call when this option is selected.
        next_menu (Optional[int]): Index of the next menu to display after selection.
    """
    title: str
    option: str
    action: Optional[Callable[[str], None]] = None
    next_menu: Optional[int] = None


@dataclass
class Menu:
    """
    Represents a menu screen with multiple options.

    Attributes:
        title (str): Title of the menu.
        options (List[MenuOption]): List of selectable menu options.
    """
    title: str
    options: List[MenuOption]


class EndpointTester:
    """
    Main class handling the terminal UI for API endpoint testing.

    Attributes:
        stdscr: The main curses screen object.
        menu_status (bool): Whether the menu loop is active.
        current_menu (int): Index of the current menu.
        selected_option (int): Index of the currently highlighted option.
        results (List[str]): Log of test results or messages.
        menus (List[Menu]): All defined menus.
        selected_result (Dict): Stores the final selected test option details.
    """

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.menu_status = True
        self.current_menu = 0
        self.selected_option = 0
        self.results: List[str] = []
        self.selected_result: Dict = {}
        self.menus = self.define_menus()
        self.setup_curses()

    def setup_curses(self) -> None:
        """Configure curses environment and colors."""
        curses.curs_set(0)  # Hide the cursor for better UI experience
        self.stdscr.timeout(100)  # Non-blocking input with 100ms timeout
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Selected option highlight
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Titles and headers
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Success/welcome messages

    def define_menus(self) -> List[Menu]:
        """
        Define all menus and options in the application.

        Returns:
            List[Menu]: List of Menu objects representing the navigation.
        """
        manual_options = [
            MenuOption("All", "all", action=self.run_all_manual_tests)
        ]
        # Add JSON files as manual test options dynamically
        manual_options += [
            MenuOption(json_path.split('\\')[-1], json_path, action=self.run_manual_test)
            for json_path in get_manual_test_json_list()
        ]
        manual_options.append(MenuOption("Back", "back", next_menu=0))

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
                options=manual_options
            )
        ]

    def display_welcome(self) -> None:
        """Display a welcome message at startup."""
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
        """Render the current menu and options with highlights."""
        self.stdscr.clear()
        menu = self.menus[self.current_menu]

        # Title with border
        title = f" {menu.title} "
        border_line = "*" * (len(title) + 4)
        self.stdscr.addstr(0, 0, border_line, curses.color_pair(2))
        self.stdscr.addstr(1, 2, title, curses.color_pair(2) | curses.A_BOLD)
        self.stdscr.addstr(2, 0, border_line, curses.color_pair(2))

        # Options list with highlight for selection
        for idx, option in enumerate(menu.options):
            y_pos = idx + 4
            prefix = "> " if idx == self.selected_option else "  "
            if idx == self.selected_option:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y_pos, 2, f"{prefix}{option.title}")
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y_pos, 2, f"{prefix}{option.title}")

        # Footer instructions
        self.stdscr.addstr(len(menu.options) + 5, 2, "Use ↑↓ to navigate, Enter to select", curses.A_DIM)
        self.stdscr.refresh()

    def run_manual_test(self, option: str) -> None:
        """Execute a manual test using a specified JSON test file."""
        self.results.append(f"Running manual test for {option}")
        self.display_result(f"Manual Test: {option} executed successfully!")

        self.selected_result = {
            'option': 'manual_test',
            'selected': option
        }
        self.exit_program('')

    def run_all_manual_tests(self, option: str) -> None:
        """Execute all manual tests found in the directory."""
        self.results.append("Running all manual tests")
        self.display_result("All Manual Tests executed successfully!")

        self.selected_result = {
            'option': 'manual_test',
            'selected': 'all'
        }
        self.exit_program('')

    def run_crud_test(self, option: str) -> None:
        """Run CRUD tests."""
        self.results.append("Running CRUD test")
        self.display_result("CRUD Test executed successfully!")

        self.selected_result = {
            'option': 'crud',
        }
        self.exit_program('')

    def run_drf_swagger_test(self, option: str) -> None:
        """Run DRF Swagger tests."""
        self.results.append("Running DRF-Swagger test")
        self.display_result("DRF-Swagger Test executed successfully!")

        self.selected_result = {
            'option': 'drf-swagger',
        }
        self.exit_program('')

    def exit_program(self, option: str) -> None:
        """
        Exit the program by displaying results and waiting for user input.

        Args:
            option (str): The selected option that triggered exit (unused).
        """
        self.stdscr.clear()
        self.stdscr.addstr(0, 2, "Test Results:", curses.color_pair(2) | curses.A_BOLD)
        for idx, result in enumerate(self.results):
            self.stdscr.addstr(idx + 2, 2, result)
        self.stdscr.addstr(len(self.results) + 3, 2, "Thank you for using Endpoint Tester!", curses.color_pair(3))
        self.stdscr.addstr(len(self.results) + 4, 2, "Press any key to exit...", curses.A_DIM)
        self.stdscr.refresh()
        self.stdscr.getch()
        self.menu_status = False

    def display_result(self, message: str) -> None:
        """
        Display a temporary result message.

        Args:
            message (str): The message to display.
        """
        self.stdscr.clear()
        self.stdscr.addstr(2, 2, message, curses.color_pair(3) | curses.A_BOLD)
        self.stdscr.addstr(4, 2, "Press any key to continue...", curses.A_DIM)
        self.stdscr.refresh()
        self.stdscr.getch()

    def run(self) -> Dict:
        """
        Run the main loop of the application.

        Returns:
            Dict: The user's selected test option details.
        """
        self.display_welcome()

        while self.menu_status:
            self.display_menu()
            try:
                key = self.stdscr.getch()
            except Exception:
                # Continue loop on input errors (e.g., window resize)
                continue

            menu = self.menus[self.current_menu]

            # Navigate menu options with arrow keys
            if key == curses.KEY_UP and self.selected_option > 0:
                self.selected_option -= 1
            elif key == curses.KEY_DOWN and self.selected_option < len(menu.options) - 1:
                self.selected_option += 1
            elif key in (curses.KEY_ENTER, 10, 13):  # Enter key
                selected = menu.options[self.selected_option]
                if selected.action:
                    selected.action(selected.option)
                if selected.next_menu is not None:
                    self.current_menu = selected.next_menu
                    self.selected_option = 0

        return self.selected_result


def main(stdscr) -> Dict:
    """
    Entry point for curses.wrapper to launch the tester UI.

    Args:
        stdscr: The curses standard screen object.

    Returns:
        Dict: Selected option info after user interaction.
    """
    tester = EndpointTester(stdscr)
    return tester.run()


if __name__ == "__main__":
    selected_option = curses.wrapper(main)

    match selected_option.get('option'):

        case 'crud':
            crud_test = EndpointCRUDUnitTesting(**crud_test_configs)
            crud_test.run_test()

        case 'drf-swagger':
            drf_test = DRFAPIUnitTesting(**drf_test_configs)
            drf_test.run_test()

        case 'manual_test':
            selected = selected_option.get('selected', '')

            if selected == 'all':
                for json_path in get_manual_test_json_list():
                    print(f'\n\nRun Test [{json_path.split("\\")[-1]}]:')
                    manual_testing = ManualEndpointUnitTesting(endpoint_json_path=json_path)
                    manual_testing.run_test()
            else:
                manual_testing = ManualEndpointUnitTesting(endpoint_json_path=selected)
                manual_testing.run_test()
