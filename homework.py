from typing import List, Dict, Tuple, Union


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

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
    M_IN_KM = 1000

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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий
        после бега."""
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        avg_speed = self.get_mean_speed()
        dur_in_min = self.duration * 60
        var_1 = coeff_calorie_1 * avg_speed - coeff_calorie_2
        spent_calories = var_1 * self.weight / self.M_IN_KM * dur_in_min
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

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
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        avg_speed = self.get_mean_speed()
        dur_in_min = self.duration * 60
        var = (avg_speed**2 // self.height) * coeff_calorie_2 * self.weight
        spent_calories = (coeff_calorie_1 * self.weight + var) * dur_in_min
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38

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
        """Получить среднюю скорость."""
        var = self.length_pool * self.count_pool
        mean_speed = var / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить затраченное количество калорий
        после плавания."""
        avg_speed = self.get_mean_speed()
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        var = coeff_calorie_2 * self.weight
        spent_calories = (avg_speed + coeff_calorie_1) * var
        return spent_calories


def read_package(workout_type: str, data: List[Union[int, float]]) -> Training:
    """Прочитать данные полученные от датчиков."""
    code_workout: Dict[str, type] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }

    workout_object = code_workout[workout_type](*data)
    return workout_object


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages: List[Tuple[str, List[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
