import pathlib


class NormLab:
    def __init__(self, homeworksPath: str) -> None:
        # 读取 id
        self.__lab_id = pathlib.Path(homeworksPath).name.split("-")[0]

    def get_lab_id(self) -> int:
        return self.__lab_id


if __name__ == '__main__':
    pass
