import csv
import os
import pathlib
import typing

import extractor
import student

from student import Student


class NormLab:
    def __init__(self, homeworks_path: str, result_dir: str, student_repo: student.AbstractStudentRepo) -> None:
        self.__homeworks_path = homeworks_path
        self.__lab_id = pathlib.Path(self.__homeworks_path).name.split("-")[0]
        self.__result_dir = result_dir + "/" + self.__lab_id  # 结果输出路径
        self.student_repo = student_repo

    def extract_source_homework(self) -> None:
        """
        解压作业
        """
        homeworks_extractor = None
        homeworks_path_obj = pathlib.Path(self.__homeworks_path)

        if homeworks_path_obj.suffix == ".zip":
            homeworks_extractor = extractor.UnZip
        elif homeworks_path_obj.suffix == ".rar":
            homeworks_extractor = extractor.UnRar

        # 解压原始文件
        with homeworks_extractor(self.__homeworks_path, self.__result_dir) as e:
            e.extract()

        # 对每个学生的文件进行解压
        for root, dirs, files in os.walk(self.__result_dir):
            for file in files:
                # 解压当前文件
                path_obj = pathlib.Path(os.path.join(root, file))
                student_id = path_obj.name.split('-')[0]
                student_obj = self.student_repo.get_student(student_id)
                student_dir_path = root + "/" + self.__lab_id + "-" + student_id + "-" + student_obj.get_short_name()

                # 开始解压
                if path_obj.suffix == ".zip":
                    homeworks_extractor = extractor.UnZip
                elif path_obj.suffix == ".rar":
                    homeworks_extractor = extractor.UnRar
                else:
                    continue
                with homeworks_extractor(os.path.join(root, file),
                                         student_dir_path) as e:
                    e.extract()

                os.remove(os.path.join(root, file))

        # 对学生的子文件夹进行解压
        for root, dirs, files in os.walk(self.__result_dir):
            for file in files:
                # 解压当前文件
                path_obj = pathlib.Path(os.path.join(root, file))
                if path_obj.suffix == ".zip":
                    homeworks_extractor = extractor.UnZip
                elif path_obj.suffix == ".rar":
                    homeworks_extractor = extractor.UnRar
                else:
                    continue

                with homeworks_extractor(os.path.join(root, file),
                                         root + "/" + path_obj.name.split(".")[0]) as e:
                    dirs.append(root + "/" + path_obj.name.split(".")[0])
                    e.extract()

                os.remove(os.path.join(root, file))

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


if __name__ == '__main__':
    pass
