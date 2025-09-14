
import hashlib
import cmd


input_string = "my-secret-password"
sha256_hash = hashlib.sha256(input_string.encode()).hexdigest()
print(sha256_hash)

class HashCLI(cmd.Cmd):
    intro = "Welcome to the SHA256 CLI. Type 'hash' to hash a string or 'exit' to quit."
    prompt = "(sha256-cli) "

    def do_hash(self, arg):
        """Hash a string using SHA256. Usage: hash"""
        user_input = input("Enter a string to hash: ")
        sha256_hash = hashlib.sha256(user_input.encode()).hexdigest()
        print(f"SHA256: {sha256_hash}")
    
    def do_exit(self, arg):
        """Exit the CLI"""
        print("Goodbye!")
        return True

    def do_quit(self, arg):
        """Exit the CLI (alias for exit)"""
        return self.do_exit(arg)
        
        
if __name__ == "__main__":
    HashCLI().cmdloop()