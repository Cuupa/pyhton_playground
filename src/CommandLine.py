class CommandLine:
    path_to_save = None
    urls = None

    def __init__(self, args):
        self.parse_command_line_arguments(args)

    def parse_command_line_arguments(self, args):
        if "--help" in args:
            self.print_help()

        if "--out=" in args:
            self.handle_out_arg(args)

        if "--url=" in args:
            self.handle_url_arg(args)

    def handle_url_arg(self, args):
        urls_arg = args.split("=")
        if len(urls_arg) == 2:
            global urls
            urls = urls_arg[1]
        else:
            self.print_help()
            exit()

    def handle_out_arg(self, args):
        out_arg = args.split("=")
        if len(out_arg) == 2:
            global path_to_save
            path_to_save = out_arg[1]
        else:
            self.print_help()
            exit()

    def print_help(self):
        print("--help\t\t\t\t\tPrints this screen.")
        print("--url=www.amazon.com/product_id\t\tThe url which shall be processed")
        print("\t\t\t\t\tIf no url is specified, the program will use the hardcoded ones.")
        print(
            "--out=/path/to/save/to\t\t\tThe directory to save to. If the directory doesn\'t exist it will be created.")
        print("\t\t\t\t\tIf no output directory is specified, the files will be saved next to the program.")
        exit()
