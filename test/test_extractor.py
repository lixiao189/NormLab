import contextlib
import shutil
import os

import extractor


def test_unzip():
    """
    测试解压 zip 文件, 检查某个学生的文件是否被解压出来
    """
    source_file_path = "../data/Lab03-JUnit for Unit Test.zip"
    target_dir_path = "../result"

    a_student_file_name = "L201926630134-HOMWEYETSUROMARTIN.zip"

    with extractor.UnZip(source_file_path, target_dir_path) as unzip:
        unzip.extract()

        for root, dirs, files in os.walk(target_dir_path):
            assert a_student_file_name in files
            break

        # 删除临时文件
        shutil.rmtree(target_dir_path)


def test_unrar():
    """
    测试解压 rar 文件
    """
    source_file_path = "../data/test.rar"
    target_dir_path = "../result"

    file_dir_name = "test"

    with extractor.UnRar(source_file_path, target_dir_path) as unrar:
        unrar.extract()

        for root, dirs, files in os.walk(target_dir_path):
            assert file_dir_name in dirs
            break

        # 删除临时文件
        shutil.rmtree(target_dir_path)


def test_extract_test_case1():
    sourcefile_path = "../data/test-case-01/Lab01-中文.zip"
    target_path = "../result"

    with contextlib.suppress(FileNotFoundError):
        shutil.rmtree(target_path)
    with extractor.ExtractorFactory(sourcefile_path, target_path).get_extractor() \
            as file_extractor:
        file_extractor.extract()
