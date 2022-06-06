from thefuzz import fuzz

import os
import pathlib
import shutil
import sys
import typing

import extractor
import student


class NormLab:
    def __init__(self, homeworks_path: str, result_dir: str, student_repo: student.AbstractStudentRepo,
                 reporter: student.AbstractSimilarReporter) -> None:
        self.__homeworks_path = homeworks_path
        self.__lab_id = pathlib.Path(self.__homeworks_path).name.split("-")[0]
        self.__result_dir = result_dir + "/" + self.__lab_id  # 结果输出路径
        self.__student_repo = student_repo
        self.__similar_group = student.SimilarGroup(self.__student_repo)  # 判断是否有相同情况的并查集
        self.__similar_reporter = reporter

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
                student_obj = self.__student_repo.get_student(student_id)
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
        """
        移动报告文件到指定目录
        """
        homework_list = os.listdir(self.__result_dir)

        for homework_dir in homework_list:
            # 获取学生对象
            student_id = homework_dir.split("-")[1]
            student_obj = self.__student_repo.get_student(student_id)
            report_file_name = self.__lab_id + "-" + student_id + "-" + student_obj.get_short_name() + ".docx"

            # 处理报告 docx 文件
            for root, dirs, files in os.walk(os.path.join(self.__result_dir, homework_dir)):
                for filename in files:
                    if pathlib.Path(os.path.join(root, filename)).suffix == ".docx":
                        os.rename(os.path.join(root, filename), os.path.join(root, report_file_name))
                        shutil.move(os.path.join(root, report_file_name), self.__result_dir)

    def remove_repetitive_dir(self) -> None:
        """
        处理 A / A 这种情况的文件夹 (相似文件夹也要处理)
        """
        for root, dirs, files in os.walk(self.__result_dir):
            for dirname in dirs:
                son_dirs = os.listdir(os.path.join(root, dirname))
                if len(son_dirs) == 1:  # 如果只有一个子文件夹
                    # debug
                    print(dirname, son_dirs[0])
                    print(fuzz.ratio(dirname, son_dirs[0]))

                    if fuzz.ratio(dirname, son_dirs[0]) >= 50:  # 相似度在 50% 以上
                        # delete file
                        father_dir_name = dirname
                        temp_name = "dir_deleted"

                        os.rename(os.path.join(root, dirname), os.path.join(root, temp_name))
                        shutil.move(os.path.join(root, temp_name, son_dirs[0]), os.path.join(root))
                        os.rename(os.path.join(root, son_dirs[0]), os.path.join(root, father_dir_name))
                        dirs.append(father_dir_name)  # 添加新文件夹进入 dirs 列表，让 os.walk 函数遍历
                        shutil.rmtree(os.path.join(root, temp_name))

    def generate_similar_report(self) -> None:
        student_has_homework: typing.List[student.Student] = []

        # 找出所有交了作业的人
        for item in os.listdir(self.__result_dir):
            if pathlib.Path(os.path.join(self.__result_dir, item)).is_dir():
                tmp_student = self.__student_repo.get_student(item.split("-")[1])
                student_has_homework.append(tmp_student)

        # 两两比对
        for s1 in student_has_homework:
            for s2 in student_has_homework:
                if s1.get_stu_id() == s2.get_stu_id():
                    continue
                s1_homework_dir = self.__lab_id + "-" + s1.get_stu_id() + "-" + s1.get_short_name()
                s2_homework_dir = self.__lab_id + "-" + s2.get_stu_id() + "-" + s2.get_short_name()

                # 开始比较两个人的作业
                similar_file_name = True
                similar_file_size = True
                file_size: typing.Dict[str, int] = dict()
                for root, dirs, files in os.walk(os.path.join(self.__result_dir, s1_homework_dir)):
                    for filename in files:
                        file_size[filename] = os.stat(os.path.join(root, filename)).st_size

                for root, dirs, files in os.walk(os.path.join(self.__result_dir, s2_homework_dir)):
                    for filename in files:
                        if filename not in file_size:
                            similar_file_name = False
                        elif file_size[filename] != os.stat(os.path.join(root, filename)).st_size:
                            # 如果同名文件文件尺寸不一样
                            similar_file_size = False

                if similar_file_size:
                    self.__similar_group.union_with_reason(s1.get_stu_id(), s2.get_stu_id(),
                                                           student.SimilarReason.SIMILAR_SIZE)
                if similar_file_name:
                    self.__similar_group.union_with_reason(s1.get_stu_id(), s2.get_stu_id(),
                                                           student.SimilarReason.SIMILAR_NAME)

        rows = []
        for key in self.__similar_group.get_similar_reason():
            row = []
            if not len(self.__similar_group.get_similar_reason()[key]) == 0:
                row.append(key)
                for reason in self.__similar_group.get_similar_reason()[key]:
                    row.append(reason)

                rows.append(row)

        self.__similar_reporter.generate_reporter(rows)

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

    try:
        shutil.rmtree(homeworks_result_dir)  # 删除之前的结果
    except FileNotFoundError:
        pass

    with student.CSVStudentRepo(students_list_path) as repo, \
            student.CSVSimilarReporter(homeworks_result_dir) as similar_reporter:
        normlab_obj = NormLab(homeworks_file_path, homeworks_result_dir, repo, similar_reporter)

        normlab_obj.extract_source_homework()
        normlab_obj.delete_extra_files()
        normlab_obj.move_reports()
        normlab_obj.remove_repetitive_dir()
        # normlab_obj.generate_similar_report()
