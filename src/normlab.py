import os
import pathlib
import shutil
import typing

import extractor
import student


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

    def delete_extra_files(self) -> None:
        """
        删除多余的文件
        """
        extra_dir_list: typing.List[str] = [
            ".idea",
            ".vscode",
            "target",
        ]
        extra_file_list: typing.List[str] = [
            "计算机科学与技术学院-软件工程（留学生）-2019软件工程（留学生）",
            ".class"
        ]

        for root, dirs, files in os.walk(self.__result_dir):
            for dirname in dirs:
                if dirname in extra_dir_list:
                    shutil.rmtree(os.path.join(root, dirname))

            for filename in files:
                for file_should_delete in extra_file_list:
                    if file_should_delete in filename:
                        os.remove(os.path.join(root, filename))

        # 处理有人上传了两份报告的情况
        homework_list = os.listdir(self.__result_dir)
        for homework_dir in homework_list:  # 开始对每个人的作业文件进行处理
            docx_file_list = []
            # 查找所有的 docx 文件
            for root, dirs, files in os.walk(os.path.join(self.__result_dir, homework_dir)):
                for filename in files:
                    if pathlib.Path(os.path.join(root, filename)).suffix == ".docx":
                        docx_file_list.append(os.path.join(root, filename))

            # 删除多余的 docx 文件
            if len(docx_file_list) > 1:
                for i in range(0, len(docx_file_list) - 1):
                    os.remove(docx_file_list[i])

    def move_reports(self) -> None:
        for root, dirs, files in os.walk(self.__result_dir):
            for filename in files:
                if pathlib.Path(os.path.join(root, filename)).suffix == ".docx":
                    print(os.path.join(root, filename))  # debug

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
