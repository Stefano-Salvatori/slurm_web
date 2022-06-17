import os

class CommandExecutor:
    def execute(self, command:str) -> str:
        return os.popen(command).read()