"""车牌生成器，自动去重并持久化到文件"""

import os
import string
import random


class PlateGenerator:
    """车牌生成器，自动去重并持久化到文件"""

    def __init__(self):
        from data_factory import data_path
        self._plate_file = data_path("licenseplate")
        self._existing_plates = None

    def _load_plates(self):
        """从文件加载已生成的车牌集合，不存在则自动创建"""
        if not os.path.exists(self._plate_file):
            open(self._plate_file, 'w', encoding='utf-8').close()
            return set()
        with open(self._plate_file, 'r', encoding='utf-8') as f:
            return {line.strip() for line in f if line.strip()}

    def _save_plates(self, new_plates):
        """将新生成的车牌追加到文件"""
        with open(self._plate_file, 'a', encoding='utf-8') as f:
            for plate in new_plates:
                f.write(plate + '\n')

    def generate(self, count):
        """
        生成指定数量的不重复随机车牌，自动全局去重并持久化
        :param count: 车牌个数；传入 "clear" 清空所有已生成记录
        :return: 逗号分隔的车牌字符串，如 "浙A8529K,京B12345"
        """
        if self._existing_plates is None:
            self._existing_plates = self._load_plates()

        if count == "clear":
            self._existing_plates.clear()
            open(self._plate_file, 'w', encoding='utf-8').close()
            return ""

        count = int(count)
        if count <= 0:
            return ""

        max_total = 500
        if len(self._existing_plates) + count > max_total:
            count = max_total - len(self._existing_plates)
            if count <= 0:
                return ""

        provinces = '京津冀晋蒙辽吉黑沪苏浙皖闽赣鲁豫鄂湘粤桂琼川贵云藏陕甘青宁新渝'
        letters = string.ascii_uppercase.replace('I', '').replace('O', '')
        new_plates = []

        while len(new_plates) < count:
            province = random.choice(provinces)
            letter = random.choice(letters)
            suffix = ''.join(random.choices(string.digits + letters, k=5))
            plate = f"{province}{letter}{suffix}"
            if plate not in self._existing_plates:
                self._existing_plates.add(plate)
                new_plates.append(plate)

        self._save_plates(new_plates)
        return ','.join(new_plates)
