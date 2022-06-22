import os
from typing import List


class CommandExecutor:
    def execute(self, command: str, split_new_lines: bool = False) -> str:
        command_result = os.popen(command).read()
        return self.__split_new_lines(command_result) if split_new_lines else command_result

    def __split_new_lines(self, command_result: str) -> List[str]:
        splitted = command_result.split(os.linesep)
        # we drop the last line if is empty
        return splitted[:-1] if splitted[-1] == "" else splitted

