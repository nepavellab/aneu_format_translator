import sys
import re


class FormatTranslator:
    """\
    This class translates a file along the specified path from ".neu(.nue)" format to ".aneu(.nue)" format.
    The absolute path to the file with specifying the extension is passed to the class constructor.

    EXAMPLE:
    --- \"C:\\\\Users\\\\Asus\\\\Mesh.nue\" (or \"...\\\\Mesh.neu\")

    As already indicated in the example, after successful execution of the program,
    the file ".anue" will be created in the same directory as the file ".neu(.nue)"

    IMPORTANT: when starting in the Windows operating system, enter the file name with a double backslash, as shown in the example
    """
    def __init__(self, file_path: str) -> None:
        try:
            self.__file_n = open(file_path, "rb")
            #  extension check (.nue or .neu)
            if file_path[-2] == "u":
                self.__file_an = open(file_path[0:-3] + "anue", "wb")
            else:
                self.__file_an = open(file_path[0:-3] + "aneu", "wb")

            #  node information block
            self.__load(0, True)
            #  finite element information block
            self.__load(1, False)
            #  surface finite element information block
            self.__load(1, False)
            
            self.__file_n.close()
            self.__file_an.close()

            #  the program ran successfully without errors
            print(">>> *.aneu file created\n")
        except FileNotFoundError:
            print("Cannot open \".nue\" file by path:", file_path, "\n>>> FAIL\n")
        except OSError:
            print(">>> FAIL\n")

    def __load(self, start_limit: int, is_float: bool) -> None:
        #  the first line of the block, storing the number of lines
        #  with information (coordinates of nodes or node IDs of finite elements)
        count: str = bytes.decode(self.__file_n.readline(), encoding="utf-8")
        
        #  read the first line of the block with information
        #  about nodes or elements to determine the number of parameters
        first_line_parameters = bytes.decode(self.__file_n.readline(), "utf-8")

        #  create a list from a string of parameters to determine their number
        mesh_list: list[int | float] = re.findall(r"\d+\.\d+", first_line_parameters) if\
                          is_float else re.findall(r"\d+", first_line_parameters) 
 
        #  write to the ".aneu(.anue)" file a new line
        #  with the old number of lines and the added number of parameters
        self.__file_an.write((str(count.split("\r")[0]) + "\r" + str(len(mesh_list[start_limit:]))
                         + "\r\n").encode(encoding="utf-8"))
        #  move the pointer back one line
        self.__file_n.seek(-len(first_line_parameters), 1)

        #  write the remaining lines of the block to the ".aneu(.anue)" file
        for i in range(int(count)):
            self.__file_an.write(self.__file_n.readline())


FormatTranslator(sys.argv[1])

