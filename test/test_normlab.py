import os


def test_cases():
    """
    所有的测试样例放在 /data/test-cases/ 下
    所有的测试样例命名为 test-case-1 这样的编号
    test-case 中包含了一个压缩包当作测试输入，命名为 input.zip 和一个 Output-Expected 文件夹
    """

    testcase_dir = "../data/test-cases"
    for case_dir in os.listdir(testcase_dir):
        case_path = os.path.join(testcase_dir, case_dir)

