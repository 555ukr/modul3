import cmd
import sys
from termcolor import colored
sys.path.insert(0, 'src/')
from blockchain import Blockchain


class HelloWorld(cmd.Cmd):
    prompt = colored('mining-cli> ', "blue")

    def preloop(self):
        print(colored("Welcome to miner cli!", "yellow"))
        if (len(sys.argv) > 1 and sys.argv[1] == '-restart'):
            Blockchain.genesis_block()
            print(colored('Genesis block created', "cyan"))

    def do_EOF(self, line):
        return True

    def do_exit(self, inp):
            # '''exit the application.'''
        print(colored("\nBye for now", "yellow"))
        return True

    do_EOF = do_exit

if __name__ == '__main__':
    HelloWorld().cmdloop()
