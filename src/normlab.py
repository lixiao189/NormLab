import pathlib

from extractor import UnZip


class NormLab:
    def __init__(self, homeworks_path: str) -> None:
        # 读取 id
        self.__lab_id = pathlib.Path(homeworks_path).name.split("-")[0]
        self.__result_dir = "../result"  # 结果输出路径

    def get_lab_id(self) -> str:
        return self.__lab_id


if __name__ == '__main__':
    sourceHomework = UnZip(
        "/Users/node/Developer/Python/NormLab/data/Lab03-JUnit for Unit Test.zip",
        "../temp"
    )

    with UnZip(
        "/Users/node/Developer/Python/NormLab/data/Lab03-JUnit for Unit Test.zip",
        "../temp"
    ) as unzip:
        unzip.extract()
