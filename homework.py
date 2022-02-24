from dataclasses import dataclass
from typing import Dict, List, Tuple, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Создание сообщения о результатах тренировки."""
        msg = f'Тип тренировки: {self.training_type}; '
        msg += 'Длительность: {0:.3f} ч.; '.format(self.duration)
        msg += 'Дистанция: {0:.3f} км; '.format(self.distance)
        msg += 'Ср. скорость: {0:.3f} км/ч; '.format(self.speed)
        msg += 'Потрачено ккал: {0:.3f}.'.format(self.calories)
        return msg


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()
        mean_speed = distance / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            type(self).__name__,
            ': не был переопределен метод get_spent_calories!'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1: float = 18
    COEFF_CALORIE_2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий
        после бега."""
        avg_speed = self.get_mean_speed()
        dur_in_min = self.duration * self.MIN_IN_HOUR
        var_1 = self.COEFF_CALORIE_1 * avg_speed - self.COEFF_CALORIE_2
        spent_calories = var_1 * self.weight / self.M_IN_KM * dur_in_min
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить затраченное количество калорий
        после спортивной ходьбы."""
        avg_speed = self.get_mean_speed()
        dur_in_min = self.duration * self.MIN_IN_HOUR
        var_1 = (avg_speed**2 // self.height) * self.COEFF_CALORIE_2
        var_2 = var_1 * self.weight
        var_3 = self.COEFF_CALORIE_1 * self.weight
        spent_calories = (var_2 + var_3) * dur_in_min
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость во время плавания."""
        var_1 = self.length_pool * self.count_pool
        mean_speed = var_1 / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить затраченное количество калорий
        после плавания."""
        avg_speed = self.get_mean_speed()
        spent_calories = ((avg_speed + self.COEFF_CALORIE_1) *
        self.COEFF_CALORIE_2 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков
    и вернуть объект тренировки."""
    code_workout: Dict[str, Type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }

    if workout_type in code_workout:
        workout_object = code_workout[workout_type](*data)
        return workout_object
    else:
        print(f'{workout_type} - недопустимый код тренировки!')
      

def main(training: Training) -> None:
    """Главная функция."""
    try:
        print(training.show_training_info().get_message())
    except AttributeError:
        print('В функцию main был передан недопустимый объект тренировки!')


if __name__ == '__main__':
    packages: List[Tuple[str, List[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)