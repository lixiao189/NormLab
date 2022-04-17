import zipfile
import abc

import rarfile


class Extractor(abc.ABC):
    """
    一个抽象类, 约束了解压类
    """

    def __init__(self, source_path, target_path) -> None:
        self._source_path = source_path  # 压缩包文件路径
        self._target_path = target_path  # 压缩包目标路径

    @abc.abstractmethod
    def __enter__(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @abc.abstractmethod
    def extract(self) -> None:
        raise NotImplementedError


class UnZip(Extractor):
    """
    负责解压 zip 的类
    """

    def __init__(self, source_path: str, target_path: str) -> None:
        super().__init__(source_path, target_path)

    def __enter__(self) -> Extractor:  # 创建压缩文件对象
        self.__zip_file = zipfile.ZipFile(self._source_path)  # 压缩文件对象
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # 退出的时候关闭文件对象
        self.__zip_file.close()

    def extract(self) -> None:  # 解压方法
        file_list = self.__zip_file.namelist()

        for file in file_list:
            self.__zip_file.extract(file, self._target_path)


class UnRar(Extractor):
    """
    负责解压 rar 文件的类
    """

    def __init__(self, source_path: str, target_path: str) -> None:
        super().__init__(source_path, target_path)

    def __enter__(self):
        self.__rar_file = rarfile.RarFile(self._source_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.__rar_file.close()

    def extract(self) -> None:
        file_list = self.__rar_file.namelist()

        for file in file_list:
            self.__rar_file.extract(file, self._target_path)
