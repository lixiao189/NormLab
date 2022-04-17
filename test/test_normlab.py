import pathlib

import pytest
import os

import student
from normlab import NormLab


@pytest.fixture(scope="module")
def normlab_obj():
    homeworks_file_path = "../data/Lab03-JUnit for Unit Test.zip"  # 源文件路径
    homeworks_result_dir = "../temp"  # 父目录存储结果
    students_list_path = "../data/students_list.csv"

    with student.CSVStudentRepo(students_list_path) as repo:
        normlab_obj = NormLab(homeworks_file_path, homeworks_result_dir, repo)
    return normlab_obj  # 创建系统对象


def test_get_lab_id():
    lab = NormLab(
        "../data/Lab03-JUnit for Unit Test.zip"
    )

    assert lab.get_lab_id() == "Lab03"


def test_extract_source_homework(normlab_obj: NormLab):
    has_compress_file = False
    compress_file_suffix = [
        ".zip",
        ".rar"
    ]

    normlab_obj.extract_source_homework()
    for root, dirs, files in os.walk(normlab_obj.get_result_dir()):
        for file in files:
            if pathlib.Path(os.path.join(root, file)).suffix in compress_file_suffix:
                has_compress_file = True

    assert not has_compress_file
