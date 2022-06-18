import os
import pathlib
import typing
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
    def extract(self) -> typing.List[typing.Tuple[str, str]]:
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

    def extract(self) -> typing.List[typing.Tuple[str, str]]:  # 解压方法
        file_list = self.__zip_file.infolist()
        archive_file_list: typing.List[typing.Tuple[str, str]] = []

        for file in file_list:
            # 修复乱码
            with contextlib.suppress(UnicodeDecodeError, UnicodeEncodeError):
                file.filename = file.filename.encode("cp437").decode("utf-8")
            with contextlib.suppress(UnicodeDecodeError, UnicodeEncodeError):
                file.filename = file.filename.encode("cp437").decode("gbk")

            self.__zip_file.extract(file, self._target_path)

            file_path = os.path.join(self._target_path, file.filename)
            if is_archive(file_path):
                archive_file_list.append((file_path, get_target_path(file_path)))

        return archive_file_list


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

    def extract(self) -> typing.List[typing.Tuple[str, str]]:
        file_list = self.__rar_file.infolist()
        archive_file_list: typing.List[typing.Tuple[str, str]] = []

        for file in file_list:
            self.__rar_file.extract(file, self._target_path)

            file_path = os.path.join(self._target_path, file.filename)
            if is_archive(file_path):
                archive_file_list.append((file_path, get_target_path(file_path)))

        return archive_file_list


class ExtractorFactory:
    def __init__(self, source_path: str, target_path: str):
        self.__source_path = source_path
        self.__target_path = target_path

    def get_extractor(self) -> Extractor:
        if self.__source_path.split(".")[-1] == "zip":
            return UnZip(self.__source_path, self.__target_path)

        elif self.__source_path.split(".")[-1] == "rar":
            return UnRar(self.__source_path, self.__target_path)


def get_target_path(file_path: str) -> str:
    path_obj = pathlib.Path(file_path)
    return f"{path_obj.parent}/{path_obj.name.split('.')[0]}"


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


class ExtractPipeline:
    def __init__(self, source_path: str, target_path: str):
        self.__source_path = source_path
        self.__target_path = target_path
        self.__archive_file_list: typing.List[typing.Tuple[str, str]] = [(self.__source_path, self.__target_path)]

    def extract_all(self):
        for archive_file in self.__archive_file_list:
            with ExtractorFactory(archive_file[0], archive_file[1]).get_extractor() as e:
                for new_archive_file in e.extract():
                    self.__archive_file_list.append(new_archive_file)

        # 删除多余的嵌套压缩包
        for i in range(1, len(self.__archive_file_list)):
            os.remove(self.__archive_file_list[i][0])
