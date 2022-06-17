import pathlib
import zipfile
import abc

import contextlib
import rarfile


class Extractor(abc.ABC):
    """
    一个抽象类, 约束了解压类
    """

    def __init__(self, source_path: str, target_path: str) -> None:
        self._source_path = source_path  # 压缩包文件路径
        self._target_path = target_path  # 压缩包目标路径

    @abc.abstractmethod
    def __enter__(self):
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
        file_list = self.__zip_file.infolist()

        for file in file_list:
            # 修复乱码
            with contextlib.suppress(UnicodeDecodeError, UnicodeEncodeError):
                file.filename = file.filename.encode("cp437").decode("utf-8")
            with contextlib.suppress(UnicodeDecodeError, UnicodeEncodeError):
                file.filename = file.filename.encode("cp437").decode("gbk")

            self.__zip_file.extract(file, self._target_path)


class UnRar(Extractor):
    """
    负责解压 rar 文件的类
    """

    def __init__(self, source_path: str, target_path: str) -> None:
        super().__init__(source_path, target_path)

    def __enter__(self) -> Extractor:
        self.__rar_file = rarfile.RarFile(self._source_path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.__rar_file.close()

    def extract(self) -> None:
        file_list = self.__rar_file.namelist()

        for file in file_list:
            self.__rar_file.extract(file, self._target_path)


class ExtractorFactory:
    def __init__(self, source_path: str, target_path: str):
        self.__source_path = source_path
        self.__target_path = target_path

    def get_extractor(self) -> Extractor:
        if self.__source_path.split(".")[-1] == "zip":
            return UnZip(self.__source_path, self.__target_path)

        elif self.__source_path.split(".")[-1] == "rar":
            return UnRar(self.__source_path, self.__target_path)


def is_archive(file_path: str) -> bool:
    """
    判断是否是压缩包
    """
    archive_file_suffix = [
        ".zip",
        ".rar",
    ]
    path_obj = pathlib.Path(file_path)
    return path_obj.suffix in archive_file_suffix
