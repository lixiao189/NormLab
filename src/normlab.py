import contextlib
import itertools
from thefuzz import fuzz

import os
import pathlib
import shutil
import sys
import typing

import extractor
import student


class NormLab:
    def __init__(self,
                 homeworks_path: str,
                 result_dir: str,
                 student_repo: student.AbstractStudentRepo,
                 reporter: typing.Optional[student.AbstractSimilarReporter]) -> None:
        self.__homeworks_path = homeworks_path
        self.__lab_id = pathlib.Path(self.__homeworks_path).name.split("-")[0]
        self.__result_dir = f"{result_dir}/" + \
                            pathlib.Path(self.__homeworks_path).name.split(".")[0]

        self.__student_repo = student_repo
        self.__similar_group = student.SimilarGroup(
            self.__student_repo)  # 判断是否有相同情况的并查集
        self.__similar_reporter = reporter

    def __enter__(self):
        self.__student_repo.__enter__()

        if self.__similar_reporter is not None:
            self.__similar_reporter.__enter__()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__student_repo.__exit__(exc_type, exc_val, exc_tb)

        if self.__similar_reporter is not None:
            self.__similar_reporter.__exit__(exc_type, exc_val, exc_tb)

    def extract_source_homework(self) -> None:
        """
        解压作业
        """
        # 解压原始文件
        e = extractor.ExtractPipeline(self.__homeworks_path, self.__result_dir)
        e.extract_all()

    def rename_student_file_dir(self) -> None:
        """
        重命名学生文件夹
        """
        for student_dir in os.listdir(self.__result_dir):
            if fuzz.ratio(student_dir, 'L201926630102-DENNISERTANDY') >= 50 and len(student_dir.split("-")) == 2:
                # 找到学生文件夹以后开始处理
                student_id = student_dir.split('-')[0]
                student_shortname = self.__student_repo.get_student(student_id).get_short_name()

                os.rename(f"{self.__result_dir}/{student_dir}",
                          f"{self.__result_dir}/{self.__lab_id}-{student_id}-{student_shortname}")

    def delete_extra_files(self) -> None:
        """
        删除多余的文件
        """
        extra_dir_list: typing.List[str] = [
            ".idea",
            ".vscode",
            "target",
            "__MACOSX",
        ]
        extra_file_list: typing.List[str] = [
            "计算机科学与技术学院-软件工程（留学生）-2019软件工程（留学生）",
            ".class",
            ".DS_Store"
        ]

        for root, dirs, files in os.walk(self.__result_dir):
            for dirname in dirs:
                if dirname in extra_dir_list:
                    shutil.rmtree(os.path.join(root, dirname))

            for filename, file_should_delete in itertools.product(files, extra_file_list):
                if file_should_delete in filename:
                    os.remove(os.path.join(root, filename))

    def move_reports(self) -> None:
        """
        移动报告文件到指定目录
        """
        homework_list = os.listdir(self.__result_dir)
        report_file_count: typing.Dict[str, int] = {}
        report_file_id: typing.Dict[str, int] = {}

        for homework_dir in homework_list:
            # 获取学生对象
            try:
                student_id = homework_dir.split("-")[1]
                student_obj = self.__student_repo.get_student(student_id)
            except (KeyError, IndexError):
                continue

            for root, dirs, files in os.walk(os.path.join(self.__result_dir, homework_dir)):
                for filename in files:
                    if pathlib.Path(os.path.join(root, filename)).suffix == ".docx":
                        try:
                            report_file_count[filename] += 1
                        except KeyError:
                            report_file_count[filename] = 1
                            report_file_id[filename] = 1

            # 处理报告 docx 文件
            for root, dirs, files in os.walk(os.path.join(self.__result_dir, homework_dir)):
                for filename in files:
                    if pathlib.Path(os.path.join(root, filename)).suffix == ".docx":
                        report_file_name = f"{self.__lab_id}-{student_id}-{student_obj.get_short_name()}"
                        if report_file_count[filename] > 1:
                            report_file_name += f"-{str(report_file_id[filename])}"
                            report_file_id[filename] += 1
                        os.rename(os.path.join(root, filename), os.path.join(root, f"{report_file_name}.docx"))
                        shutil.move(os.path.join(root, f"{report_file_name}.docx"), self.__result_dir)

    def remove_repetitive_dir(self) -> None:
        """
        处理 A / A 这种情况的文件夹 (相似文件夹也要处理)
        """
        result_dir_root = str(pathlib.Path(self.__result_dir).parent)
        for root, dirs, files in os.walk(result_dir_root):
            for dirname in dirs:
                son_dirs = os.listdir(os.path.join(root, dirname))
                # 如果只有一个子文件夹
                if len(son_dirs) == 1 and os.path.isdir(os.path.join(root, dirname, son_dirs[0])) \
                        and fuzz.ratio(dirname, son_dirs[0]) >= 50:
                    # delete file
                    father_dir_name = dirname
                    temp_name = "dir_deleted"

                    os.rename(os.path.join(root, father_dir_name),
                              os.path.join(root, temp_name))
                    shutil.move(os.path.join(root, temp_name,
                                             son_dirs[0]), os.path.join(root))
                    os.rename(os.path.join(root, son_dirs[0]), os.path.join(
                        root, father_dir_name))
                    # 添加新文件夹进入 dirs 列表，让 os.walk 函数遍历
                    dirs.append(father_dir_name)
                    shutil.rmtree(os.path.join(root, temp_name))

    def remove_empty_dir(self) -> None:
        """
        删除空文件夹
        """
        for root, dirs, files in os.walk(self.__result_dir):
            for dirname in dirs:
                son_dirs = os.listdir(os.path.join(root, dirname))
                if len(son_dirs) == 0:
                    shutil.rmtree(os.path.join(root, dirname))

    def generate_similar_report(self) -> None:
        pass

    def handle_homework(self) -> None:
        """
        处理所有的作业压缩包的任务
        """
        self.extract_source_homework()
        self.rename_student_file_dir()
        self.delete_extra_files()
        self.move_reports()
        self.remove_repetitive_dir()
        self.remove_empty_dir()

    def get_homeworks_path(self) -> str:
        """
        获取作业源文件路径
        """
        return self.__homeworks_path

    def get_lab_id(self) -> str:
        """
        获取 lab id
        """
        return self.__lab_id

    def get_result_dir(self) -> str:
        """
        获取输出结果路径
        """
        return self.__result_dir

    def get_students_repo(self) -> student.AbstractStudentRepo:
        """
        获取学生仓库
        """
        return self.__student_repo


if __name__ == '__main__':
    if len(sys.argv) > 1:
        homeworks_file_path = sys.argv[1]  # 源文件路径
    else:
        homeworks_file_path = '../data/Lab03-JUnit for Unit Test.zip'
    homeworks_result_dir = "../result"  # 父目录存储结果
    students_list_path = "../data/students_list.csv"

    with contextlib.suppress(FileNotFoundError):
        shutil.rmtree(homeworks_result_dir)  # 删除之前的结果
    with NormLab(
            homeworks_file_path,
            homeworks_result_dir,
            student.CSVStudentRepo(students_list_path),
            None
    ) as normlab_obj:
        normlab_obj.handle_homework()  # 处理作业压缩包
