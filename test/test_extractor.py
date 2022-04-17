import shutil
import os

import extractor


def test_unzip():
    """
    测试解压 zip 文件, 检查某个学生的文件是否被解压出来
    """
    source_file_path = "../data/Lab03-JUnit for Unit Test.zip"
    target_dir_path = "../temp"

    a_student_file_name = "L201926630134-HOMWEYETSUROMARTIN.zip"

    unzip = extractor.UnZip(source_file_path, target_dir_path)
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
    target_dir_path = "../temp"

    file_dir_name = "test"

    unrar = extractor.UnRar(source_file_path, target_dir_path)
    unrar.extract()

    for root, dirs, files in os.walk(target_dir_path):
        assert file_dir_name in dirs
        break

    # 删除临时文件
    shutil.rmtree(target_dir_path)
