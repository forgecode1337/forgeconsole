# cli.py
import sys
from cmd2 import Cmd
from colorama import Fore, Style, init
from art import text2art
from forgeconsole import aes, keys

init(autoreset=True)  # Initialize colorama

class ForgeSecurityConsole(Cmd):
    intro = Fore.GREEN + text2art("ForgeSecurity", font='block') + "\n" + "Type 'help' or '?' to list commands." + Style.RESET_ALL
    prompt = Fore.YELLOW + "(forgesecurity) " + Style.RESET_ALL

    def do_aes(self, line):
        """Handle AES operations"""
        args = line.split()
        if len(args) < 5:
            self.poutput(Fore.RED + "Usage: aes <operation> <input_path> <output_path> --key <key> [--delete] [--private-key <path>]" + Style.RESET_ALL)
            return
        
        # Extract arguments
        operation = args[0]
        input_path = args[1]
        output_path = args[2]
        key = next((arg.split('=')[1] for arg in args if arg.startswith('--key=')), None)
        delete = '--delete' in args
        private_key = next((arg.split('=')[1] for arg in args if arg.startswith('--private-key=')), None)

        if not key:
            self.poutput(Fore.RED + "Error: --key argument is required." + Style.RESET_ALL)
            return
        
        # Prepare arguments for the aes main function
        aes_args = [
            'aes.py',
            operation,
            input_path,
            output_path,
            '--key', key
        ]
        if delete:
            aes_args.append('--delete')
        if private_key:
            aes_args.extend(['--private-key', private_key])

        # Run the AES tool
        self._run_external_script('forgeconsole/aes.py', aes_args)

    def do_keys(self, line):
        """Handle key operations"""
        args = line.split()
        if len(args) < 1:
            self.poutput(Fore.RED + "Usage: keys <operation>" + Style.RESET_ALL)
            return
        
        operation = args[0]
        if operation != 'generate':
            self.poutput(Fore.RED + "Error: Unsupported operation." + Style.RESET_ALL)
            return
        
        # Run the keys tool
        self._run_external_script('forgeconsole/keys.py', [])

    def _run_external_script(self, script_path, args):
        import subprocess
        result = subprocess.run(['python', script_path] + args, capture_output=True, text=True)
        self.poutput(result.stdout)
        if result.stderr:
            self.poutput(Fore.RED + result.stderr + Style.RESET_ALL)

def main():
    console = ForgeSecurityConsole()
    console.cmdloop()

def main():
    print("Starting ForgeSecurity Console...")
    console = ForgeSecurityConsole()
    console.cmdloop()


if __name__ == "__main__":
    main()
