import contextlib
import os
import shutil
import typing

import student
from normlab import NormLab
from thefuzz import fuzz


def test_cases():
    """
    所有的测试样例放在 /data/test-cases/ 下
    所有的测试样例命名为 test-case-1 这样的编号
    test-case 中包含了一个压缩包当作测试输入，命名为 input.zip 和一个 Output-Expected 文件夹
    """
    input_zip = {
        "test-case-1": "Lab01-中文.zip",
        "test-case-2": "Lab03-JUnit for Unit Test.zip",
        "test-case-3": "Lab03-JUnit for Unit Test.zip",
    }

    def get_dir_tree(dir_path: str, path_start_pos: int = 0) -> typing.Set:
        result_tree = set()
        for root, dirs, files in os.walk(dir_path):
            dirs.sort()
            files.sort()

            for _dirname in dirs:
                result_tree.add(os.path.join(root, _dirname)[path_start_pos:])

            for file in files:
                if file != "Similar Works Report.csv":
                    result_tree.add(os.path.join(root, file)[path_start_pos:])

        return result_tree

    testcase_dir = "../data/test-cases"
    for dirname in os.listdir(testcase_dir):
        if fuzz.ratio(dirname, "test-case-1") < 50 or len(dirname.split('-')) != 3:
            continue

        case_path = os.path.join(testcase_dir, dirname)
        expected_tree = get_dir_tree(os.path.join(case_path, "Output-Expected"),
                                     len("../data/test-cases/test-case-1/Output-Expected/"))

        # 使用 normlab 类来生成结果
        homeworks_file_path = os.path.join(case_path, input_zip[dirname])
        homeworks_result_dir = "../result"
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
        my_tree = get_dir_tree(homeworks_result_dir, len("../result/"))

        # debug
        print()
        print(expected_tree)
        print(my_tree)
