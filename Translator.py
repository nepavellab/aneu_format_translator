from typing import List
import re


class FormatTranslator:
    def __init__(self, file_path: str) -> None:
        self.__file_neu = open(file_path, "rb")
        self.__file_aneu = open(file_path + ".aneu", "wb")

    def convert(self) -> None:
        #  node information block
            self.__load(0, True)
            #  finite element information block
            self.__load(1, False)
            #  surface finite element information block
            self.__load(1, False)

            self.__file_neu.close()
            self.__file_aneu.close()

    def __load(self, start_limit: int, is_float: bool) -> None:
        #  the first line of the block, storing the number of lines
        #  with information (coordinates of nodes or node IDs of finite elements)
        count: str = bytes.decode(self.__file_neu.readline(), encoding="utf-8")
        
        #  read the first line of the block with information
        #  about nodes or elements to determine the number of parameters
        first_line_parameters = bytes.decode(self.__file_neu.readline(), "utf-8")

        #  create a list from a string of parameters to determine their number
        mesh_list: List[int | float] = re.findall(r"\d+\.\d+", first_line_parameters) if\
                          is_float else re.findall(r"\d+", first_line_parameters) 
 
        #  write to the ".aneu" file a new line
        #  with the old number of lines and the added number of parameters
        self.__file_aneu.write((str(count.split("\r")[0]) + " " + str(len(mesh_list[start_limit:]))
                         + "\r\n").encode(encoding="utf-8"))
        #  move the pointer back one line
        self.__file_neu.seek(-len(first_line_parameters), 1)

        #  write the remaining lines of the block to the ".aneu" file
        for i in range(int(count)):
            self.__file_aneu.write(self.__file_neu.readline())
