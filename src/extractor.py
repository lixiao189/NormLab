import zipfile
import abc

import rarfile


class Extractor(abc.ABC):
    """
    一个抽象类, 约束了解压类
    """

    def __init__(self, source_file_path: str, target_dir_path: str) -> None:
        self._source_path = source_file_path  # 压缩包文件路径
        self._target_path = target_dir_path  # 压缩包目标路径

    @abc.abstractmethod
    def extract(self) -> None:
        raise NotImplementedError


class UnZip(Extractor):
    """
    负责解压 zip 的类
    """

    def __init__(self, source_file_path: str, target_dir_path: str) -> None:
        super().__init__(source_file_path, target_dir_path)

    def extract(self) -> None:  # 解压方法
        with zipfile.ZipFile(self._source_path) as zip_file:
            file_list = zip_file.namelist()
            for file in file_list:
                zip_file.extract(file, self._target_path)


class UnRar(Extractor):
    """
    负责解压 rar 文件的类
    """

    def __init__(self, source_file_path: str, target_dir_path: str) -> None:
        super().__init__(source_file_path, target_dir_path)

    def extract(self) -> None:
        with rarfile.RarFile(self._source_path) as rar_file:
            file_list = rar_file.namelist()
            for file in file_list:
                rar_file.extract(file, self._target_path)
