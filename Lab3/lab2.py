import argparse
import json
import re
from tqdm import tqdm

parser = argparse.ArgumentParser(
    "Использование парсера для получения аргументов командной строки")
parser.add_argument("-input", type=str, default="data.txt",
                    help="Путь к файлу данных")
parser.add_argument("-output", type=str, default="result.txt",
                    help="Результат валидации данных")
args = parser.parse_args()
input_path = args.input
output_path = args.output


class File:
    """Объект класса File обрабатывает запись о научном сотруднике.

    Используется для хранения полей записи, а также их валидации.

    Attributes
    ----------
        inf : dict
            Словарь хранит записи в виде "тип данных о сотруднике": данные о сотруднике.
    """
    inf: dict

    def __init__(self, d) -> None:
        """Инициализирует экземпляр класса записи.

        Parameters
        ----------
            d : dict
                Копия списка с полями записи.
        """
        self.inf = d.copy()

    def check_email(self) -> bool:
        """Проверяет электронную почту на валидность.

        Returns
        -------
            bool:
                Результат проверки на корректность.
        """
        pattern = "^[^\s@]+@([^\s@.,]+\.)+[^\s@.,]{2,}$"
        if re.match(pattern, self.inf["email"]):
            return True
        return False

    def check_weight(self) -> bool:
        """Проверяет значение веса на валидность.

        Returns
        -------
            bool:
                Результат проверки на корректность.
        """
        if isinstance(self.inf["weight"], int):
            if 30 < self.inf["weight"] < 200:
                return True
        return False

    def check_snils(self) -> bool:
        """Проверяет номер СНИЛСа на валидность.

        Returns
        -------
            bool:
                Результат проверки на корректность.
        """
        pattern = "^\d{11}$"
        if re.match(pattern, self.inf["snils"]):
            return True
        return False

    def check_passport_number(self) -> bool:
        """Проверяет номер паспорта на валидность.

        Returns
        -------
            bool:
                Результат проверки на корректность.
        """
        if isinstance(self.inf["passport_number"], int):
            if 100000 <= self.inf["passport_number"] < 1000000:
                return True
        return False

    def check_university(self) -> bool:
        """Проверяет название университета на валидность.

        Returns
        -------
            bool:
                Результат проверки на корректность.
        """
        pattern = "^.*(?:[Тт]ех|[Уу]нивер|[Аа]кадем|[Ии]нститут|им\.|СПбГУ|МФТИ|МГ(?:Т|)У).*$"
        if re.match(pattern, self.inf["university"]):
            return True
        return False

    def check_work_experience(self) -> bool:
        """Проверяет значение опыта работы на валидность.

        Returns
        -------
            bool:
                Результат проверки на корректность.
        """
        if isinstance(self.inf["work_experience"], int):
            if 0 <= self.inf["work_experience"] < 80:
                return True
        return False

    def check_academic_degree(self) -> bool:
        """Проверяет значение академической степени на валидность.

        Returns
        -------
            bool:
                Результат проверки на корректность.
        """
        pattern = "Бакалавр|Кандидат наук|Специалист|Магистр|Доктор наук|"
        if re.match(pattern, self.inf["academic_degree"]):
            return True
        return False

    def check_worldview(self) -> bool:
        """Проверяет взгляд на мир на валидность.

        Returns
        -------
            bool:
                Результат проверки на корректность.
        """
        pattern = "^.+(?:изм|анство)$"
        if re.match(pattern, self.inf["worldview"]):
            return True
        return False

    def check_address(self) -> bool:
        """Проверяет адрес на валидность.

        Returns
        -------
            bool:
                Результат проверки на корректность.
        """
        pattern = "(?:ул\.|Аллея) (?:им[\.\s]|)[^\s]+ [^\s]*(?:\s|)\d+"
        if re.match(pattern, self.inf["address"]):
            return True
        return False


class Validator:
    """Объект класса Validator проверяет записи файла на валидность.

    Используется для сохранения валидных записей в файл и выдает результаты проверки.

    Attributes
    ----------
        data : dict
             Список записей.
    """
    data: list

    def __init__(self, inp) -> None:
        """Инициализирует экземпляр класса валидатор.

        Parameters
        ----------
            inp : str
                Путь к входному файлу с данными.
        """
        self.data = []
        tmp = json.load(open(inp, encoding="windows-1251"))
        for i in tmp:
            self.data.append(File(i.copy()))

    def validation(self, index) -> dict:
        """
        Выполняет валидацию записи по ее ключу.
        Attributes
        ----------
            index : index
                Индекс записи в списке записей

        Returns
        -------
            dict:
                Словарь вида: "вид данных о сотруднике":флаг, валидно ли значение.

        """
        result = {"email": self.data[index].check_email(), "weight": self.data[index].check_weight(),
                  "snils": self.data[index].check_snils(), "passport_number": self.data[index].check_passport_number(),
                  "university": self.data[index].check_university(),
                  "work_experience": self.data[index].check_work_experience(),
                  "academic_degree": self.data[index].check_academic_degree(),
                  "worldview": self.data[index].check_worldview(), "address": self.data[index].check_address()}
        return result.copy()

    def count_valid_records(self) -> int:
        """
        Считает число валидных записей.

        Returns
        -------
            int:
                Число валидных записей.
        """
        count_correct = 0
        for i in tqdm(range(len(self.data)), desc="Подсчёт корректных записей", ncols=100):
            if not (False in self.validation(i).values()):
                count_correct += 1
        return count_correct

    def count_invalid_records(self) -> int:
        """
        Считает число невалидных записей.

        Returns
        -------
            int:
                Число невалидных записей.
        """
        count_incorrect = 0
        for i in tqdm(range(len(self.data)), desc="Подсчёт некорректных записей", ncols=100):
            if False in self.validation(i).values():
                count_incorrect += 1
        return count_incorrect

    def result_file(self, output) -> None:
        """
            Записывает валидные записи в файл.
            Attributes
            ----------
                output : str
                    Путь к выходному файлу

            """
        tmp = []
        for i in tqdm(range(len(self.data)), desc="Запись результата валидации в файл", ncols=100):
            if not (False in self.validation(i).values()):
                tmp.append(self.data[i].inf.copy())
        json.dump(tmp, open(output, "w", encoding="windows-1251"),
                  ensure_ascii=False, sort_keys=False, indent=4)

    def count_invalid_arguments(self):
        """
        Считает число невалидных данных: электронная почта, вес, СНИЛС,
        номер паспорта, университет, опыт работы, академическая степень, взгляд
        на мир, адрес.

        Returns
        -------
            lst:
                Список с количеством невалидных парметров.
        """
        lst_res = []
        count_inv_email = 0
        count_inv_weight = 0
        count_inv_snils = 0
        count_inv_passport_number = 0
        count_inv_university = 0
        count_inv_work_experience = 0
        count_inv_academic_degree = 0
        count_inv_worldview = 0
        count_inv_address = 0
        for i in tqdm(range(len(self.data)), desc="Подсчёт некорректных записей  данных", ncols=100):
            if not self.data[i].check_email():
                count_inv_email += 1
            if not self.data[i].check_weight():
                count_inv_weight += 1
            if not self.data[i].check_snils():
                count_inv_snils += 1
            if not self.data[i].check_passport_number():
                count_inv_passport_number += 1
            if not self.data[i].check_university():
                count_inv_university += 1
            if not self.data[i].check_work_experience():
                count_inv_work_experience += 1
            if not self.data[i].check_academic_degree():
                count_inv_academic_degree += 1
            if not self.data[i].check_worldview():
                count_inv_worldview += 1
            if not self.data[i].check_address():
                count_inv_address += 1
        lst_res.append(count_inv_email)
        lst_res.append(count_inv_weight)
        lst_res.append(count_inv_snils)
        lst_res.append(count_inv_passport_number)
        lst_res.append(count_inv_university)
        lst_res.append(count_inv_work_experience)
        lst_res.append(count_inv_academic_degree)
        lst_res.append(count_inv_worldview)
        lst_res.append(count_inv_address)
        return lst_res.copy()


val = Validator(input_path)
valid = val.count_valid_records()
invalid = val.count_invalid_records()
lst_result = val.count_invalid_arguments()
val.result_file(output_path)
print("Статистика:")
print("Число валидных записей:", valid)
print("Общее число невалидных записей:", invalid)
print("Число невалидных записей 'email':", lst_result[0])
print("Число невалидных записей 'weight':", lst_result[1])
print("Число невалидных записей 'snils':", lst_result[2])
print("Число невалидных записей 'passport_number':", lst_result[3])
print("Число невалидных записей 'university':", lst_result[4])
print("Число невалидных записей 'work_experience':", lst_result[5])
print("Число невалидных записей 'academic_degree':", lst_result[6])
print("Число невалидных записей 'worldview':", lst_result[7])
print("Число невалидных записей 'address':", lst_result[8])