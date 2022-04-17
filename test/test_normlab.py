import pytest
import os

from normlab import NormLab


@pytest.fixture(scope="module")
def normlab_obj():
    homeworks_file_path = "../data/Lab03-JUnit for Unit Test.zip"  # 源文件路径
    homeworks_result_dir = "../temp"  # 父目录存储结果
    students_list_path = "../data/students_list.csv"

    return NormLab(homeworks_file_path, homeworks_result_dir, students_list_path)  # 创建系统对象


def test_get_lab_id():
    lab = NormLab(
        "../data/Lab03-JUnit for Unit Test.zip"
    )

    assert lab.get_lab_id() == "Lab03"


def test_extract_source_homework(normlab_obj: NormLab):
    normlab_obj.extract_source_homework()


def test_read_students_list(normlab_obj: NormLab):
    normlab_obj.read_students_list("../data/students_list.csv")
    assert normlab_obj.get_students()['L201926630103'].get_full_name() == "Doma Victor"
    assert not normlab_obj.get_students()['L201926630103'].get_full_name() == "Node Sans"
