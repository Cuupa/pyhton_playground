class CommandLine:
    args = None

    def __init__(self, args):
        self.args = args
        for arg in self.args[1::]:
            if "--help" in args:
                self.print_help()

    def is_verbose(self):
        for arg in self.args[1::]:
            if "--verbose" in arg:
                return True
        return False

    def is_hourly(self):
        for arg in self.args[1::]:
            if "--hourly" in arg:
                return True
        return False

    def get_path_to_save(self):
        for arg in self.args[1::]:
            if "--out=" in arg:
                return self.handle_out_arg(arg)
        return None

    def get_urls(self):
        for arg in self.args[1::]:
            if "--url=" in arg:
                return self.handle_url_arg(arg)
        return None

    def handle_url_arg(self, args):
        urls_arg = args.split("--url=")
        if len(urls_arg) == 2:
            return urls_arg[1]
        else:
            self.print_help()
            exit()

    def handle_out_arg(self, args):
        out_arg = args.split("--out=")
        if len(out_arg) == 2:
            return out_arg[1]
        else:
            self.print_help()
            exit()

    def print_help(self):
        print("--help\t\t\t\t\tPrints this screen.")
        print("--hourly\t\t\t\tRuns this program every hour.")
        print("--url=www.amazon.com/product_id\t\tThe url which shall be processed")
        print("\t\t\t\t\tIf no url is specified, the program will use the hardcoded ones.")
        print(
            "--out=/path/to/save/to\t\t\tThe directory to save to. If the directory doesn\'t exist it will be created.")
        print("\t\t\t\t\tIf no output directory is specified, the files will be saved next to the program.")
        exit()
