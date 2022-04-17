class Student:
    def __init__(self, stu_id: str, full_name: str, short_name: str) -> None:
        self.__stu_id = stu_id
        self.__full_name = full_name
        self.__short_name = short_name

    # getters
    def get_stu_id(self) -> str:
        return self.__stu_id

    def get_full_name(self) -> str:
        return self.__full_name

    def get_short_name(self) -> str:
        return self.__short_name