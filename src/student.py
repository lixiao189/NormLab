import abc
import csv
import typing


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


class AbstractStudentRepo(abc.ABC):
    """
    约束学生仓库的抽象类
    """

    @abc.abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @abc.abstractmethod
    def get_student(self, stu_id) -> Student:
        raise NotImplementedError


class CSVStudentRepo(AbstractStudentRepo):
    """
    从 csv 中读取学生信息
    """

    def __init__(self, csv_path: str) -> None:
        self.__students: typing.Dict[str, Student] = dict()
        self.__csv_path: str = csv_path

    def __enter__(self) -> AbstractStudentRepo:
        self.__csv_file = open(self.__csv_path)

        # 从 csv 文件中读取数据
        csv_reader = csv.reader(self.__csv_file)
        _ = next(csv_reader)
        for row in csv_reader:
            self.__students[row[0]] = Student(row[0], row[1], row[2])

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__csv_file.close()

    def get_student(self, stu_id) -> Student:
        return self.__students[stu_id]
