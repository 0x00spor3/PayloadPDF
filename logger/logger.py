class OutputManager:
    """
    Class to manage colored console output
    """
    
    # ANSI color codes
    COLORS = {
        'GREEN': '\033[92m',      # Bright green
        'ORANGE': '\033[93m',     # Bright yellow (appears orange in most terminals)
        'WHITE': '\033[97m',      # Bright white
        'RESET': '\033[0m'        # Reset to default color
    }
    
    def __init__(self, enable_colors=True):
        """
        Initialize OutputManager
        
        Args:
            enable_colors (bool): Enable/disable colored output
        """
        self.enable_colors = enable_colors
    
    def _print_colored(self, message, color_code):
        """
        Internal method to print colored text
        
        Args:
            message (str): Message to print
            color_code (str): ANSI color code
        """
        if self.enable_colors:
            print(f"{color_code}{message}{self.COLORS['RESET']}")
        else:
            print(message)
    
    def print_success(self, message):
        """
        Print success message in green color
        
        Args:
            message (str): Success message to print
        """
        self._print_colored(f"✅ {message}", self.COLORS['GREEN'])
    
    def print_warning(self, message):
        """
        Print warning message in orange color
        
        Args:
            message (str): Warning message to print
        """
        self._print_colored(f"⚠️  {message}", self.COLORS['ORANGE'])
    
    def print_info(self, message):
        """
        Print info message in white color
        
        Args:
            message (str): Info message to print
        """
        self._print_colored(f"ℹ️  {message}", self.COLORS['WHITE'])
    
    def print_error(self, message):
        """
        Bonus method: Print error message in red color
        
        Args:
            message (str): Error message to print
        """
        self._print_colored(f"❌ {message}", '\033[91m')  # Bright red
    
    def disable_colors(self):
        """Disable colored output"""
        self.enable_colors = False
    
    def enable_colors(self):
        """Enable colored output"""
        self.enable_colors = True

    # Aggiungi questo metodo alla classe OutputManager
    # Aggiungi questo metodo alla classe OutputManager esistente
    def print_banner(self):
        """Print PAYLOADPDF banner in purple"""
        banner_lines = [
            "██████╗  █████╗ ██╗   ██╗██╗      ██████╗  █████╗ ██████╗ ██████╗ ██████╗ ███████╗",
            "██╔══██╗██╔══██╗╚██╗ ██╔╝██║     ██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝",
            "██████╔╝███████║ ╚████╔╝ ██║     ██║   ██║███████║██║  ██║██████╔╝██║  ██║█████╗  ",
            "██╔═══╝ ██╔══██║  ╚██╔╝  ██║     ██║   ██║██╔══██║██║  ██║██╔═══╝ ██║  ██║██╔══╝  ",
            "██║     ██║  ██║   ██║   ███████╗╚██████╔╝██║  ██║██████╔╝██║     ██████╔╝██║     ",
            "╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═════╝ ╚═╝     ",
            "                                                                                  "
        ]

        print()
        for line in banner_lines:
            self._print_colored(line, '\033[95m')  # Purple
        print()

        # Center the subtitle
        banner_width = len(banner_lines[0])  # Use first line length as reference
        subtitle_centered = "PDF Steganography Tool v1.0".center(banner_width)
        print(f"{self.COLORS['ORANGE']}{subtitle_centered}{self.COLORS['RESET']}")
        print()
        subtitle_centered = "Made by Spor3".center(banner_width)
        print(f"{self.COLORS['WHITE']}{subtitle_centered}{self.COLORS['RESET']}")
        print()