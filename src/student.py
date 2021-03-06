import abc
import csv
import enum
import os
import pathlib
import typing


class SimilarReason(enum.Enum):
    """
    关于雷同的原因的 enum 类型
    """
    SIMILAR_SIZE = enum.auto()
    SIMILAR_NAME = enum.auto()
    SIMILAR_STRUCT = enum.auto()


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

    @abc.abstractmethod
    def get_all_students(self) -> typing.List[Student]:
        raise NotImplementedError


class CSVStudentRepo(AbstractStudentRepo):
    """
    从 csv 中读取学生信息
    """

    def __init__(self, csv_path: str) -> None:
        self.__students: typing.Dict[str, Student] = {}
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

    def get_all_students(self) -> typing.List[Student]:
        return [self.__students[key] for key in self.__students]


class AbstractSimilarReporter(abc.ABC):
    @abc.abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @abc.abstractmethod
    def generate_reporter(self, report_data: typing.List[typing.List[str]]):
        raise NotImplementedError


class CSVSimilarReporter(AbstractSimilarReporter):
    """
    使用 csv 生成雷同报告
    """

    def __init__(self, output_path: str):
        pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)

        file_path = f"{output_path}/SimilarWorksReport.csv"
        file = pathlib.Path(file_path)
        file.touch(exist_ok=True)

        self.__csv_file = open(file, 'w+', newline='')
        self.__csv_writer = csv.writer(self.__csv_file)

    def __enter__(self) -> AbstractSimilarReporter:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__csv_file.close()

    def generate_reporter(self, report_data: typing.List[typing.List[str]]) -> None:
        for row in report_data:
            self.__csv_writer.writerow(row)


class SimilarGroup:
    """
    一个并查集用来合并抄袭的一组人
    """

    def __init__(self, stu_repo: AbstractStudentRepo) -> None:
        """
        初始化并查集
        """
        self.__similar_set: typing.Dict[str, str] = {}
        self.__similar_reason: typing.Dict[str, set] = {}

        for student in stu_repo.get_all_students():
            self.__similar_set[student.get_stu_id()] = student.get_stu_id()
            self.__similar_reason[student.get_stu_id()] = set([])

    def find(self, stu_id: str) -> str:
        """
        并查集的查找
        """
        if self.__similar_set[stu_id] != stu_id:
            self.__similar_set[stu_id] = self.find(self.__similar_set[stu_id])
        return self.__similar_set[stu_id]

    def union(self, stu_id1, stu_id2) -> None:
        """
        合并两个人
        """
        father1 = self.find(stu_id1)
        father2 = self.find(stu_id2)

        self.__similar_set[father1] = father2

    def union_with_reason(self, stu_id1, stu_id2, reason):
        # 处理原因
        for origin_reason in self.__similar_reason[stu_id1]:
            self.__similar_reason[stu_id2].add(origin_reason)
        for origin_reason in self.__similar_reason[stu_id2]:
            self.__similar_reason[stu_id1].add(origin_reason)

        self.__similar_reason[stu_id1].add(reason)
        self.__similar_reason[stu_id2].add(reason)

        self.union(stu_id1, stu_id2)

    # getters
    def get_similar_set(self) -> typing.Dict[str, str]:
        return self.__similar_set

    def get_similar_reason(self) -> typing.Dict[str, set]:
        return self.__similar_reason
