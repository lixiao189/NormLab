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


def test_get_lab_id():
    lab = NormLab(
        "../data/Lab03-JUnit for Unit Test.zip"
    )

    assert lab.get_lab_id() == "Lab03"


def test_extract_source_homework(normlab_obj: NormLab):
    """
    测试解压作业文件夹
    """
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


def test_delete_extra_files(normlab_obj: NormLab) -> None:
    """
    检测是否还有多余的文件夹
    """
    normlab_obj.delete_extra_files()

    has_extra_dir = False
    extra_dir_list: typing.List[str] = [
        ".idea",
        ".vscode",
        "target",
    ]
    for root, dirs, files in os.walk(normlab_obj.get_result_dir()):
        for dirname in dirs:
            if dirname in extra_dir_list:
                has_extra_dir = True

    assert not has_extra_dir


def test_move_reports(normlab_obj: NormLab) -> None:
    students = normlab_obj.get_students_repo().get_all_students()
    report_missing = False

    # 生成所有人的报告文件名
    report_names = []
    for student_obj in students:
        report_names.append(
            normlab_obj.get_lab_id() + "-" + student_obj.get_stu_id() + "-" + student_obj.get_short_name())

    normlab_obj.move_reports()
    file_dir_list = os.listdir(normlab_obj.get_result_dir())

    for report_name in report_names:
        if report_name in file_dir_list and (report_name + ".docx") not in file_dir_list:
            report_missing = True

    assert not report_missing
