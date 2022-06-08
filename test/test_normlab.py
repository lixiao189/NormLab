import pathlib
import typing

import pytest
import os

import student
from normlab import NormLab


@pytest.fixture(scope="module")
def normlab_obj():
    homeworks_file_path = "../data/Lab03-JUnit for Unit Test.zip-JUnit for Unit Test.zip"  # 源文件路径
    homeworks_result_dir = "../result"  # 父目录存储结果
    students_list_path = "../data/students_list.csv"

    with student.CSVStudentRepo(students_list_path) as repo, student.CSVSimilarReporter(
            homeworks_result_dir) as similar_reporter:
        normlab_obj = NormLab(homeworks_file_path, homeworks_result_dir, repo, similar_reporter)
    return normlab_obj  # 创建系统对象


