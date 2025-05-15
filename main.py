import os
import sys
import matplotlib.pyplot as plt
from fuzzy_logic import FuzzyGradeSystem
from utils import save_result_json, save_result_csv, load_results_json, load_results_csv

def clear_screen():
    """Очищает экран терминала"""
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_input(prompt, min_val=0, max_val=10):
    """
    Проверяет ввод числа в заданном диапазоне
    
    :param prompt: приглашение для ввода
    :param min_val: минимальное значение
    :param max_val: максимальное значение
    :return: введенное число
    """
    while True:
        try:
            value = float(input(prompt))
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Ошибка: значение должно быть в диапазоне от {min_val} до {max_val}.")
        except ValueError:
            print("Ошибка: введите число.")

def evaluate_student():
    """
    Оценивает знания студента на основе введенных данных
    """
    clear_screen()
    print("=== Оценка знаний студента ===")
    
    # Получение данных о студенте
    student_name = input("Введите имя студента: ")
    
    # Получение параметров оценки
    quality = validate_input("Введите качество выполнения работы (0-10): ")
    accuracy = validate_input("Введите точность полученного результата (0-10): ")
    deadline = validate_input("Введите соблюдение сроков (0-10): ")
    
    # Оценка знаний
    fuzzy_system = FuzzyGradeSystem()
    numeric_grade, text_grade = fuzzy_system.evaluate(quality, accuracy, deadline)
    
    # Вывод результата
    print("\nРезультат оценки:")
    print(f"Студент: {student_name}")
    print(f"Числовая оценка: {numeric_grade:.2f}")
    print(f"Текстовая оценка: {text_grade}")
    
    # Сохранение результата
    save_result_json(student_name, quality, accuracy, deadline, numeric_grade, text_grade)
    save_result_csv(student_name, quality, accuracy, deadline, numeric_grade, text_grade)
    
    # Визуализация результата
    fig = fuzzy_system.visualize_result(quality, accuracy, deadline)
    plt.show()
    
    input("\nНажмите Enter для продолжения...")

def visualize_functions():
    """
    Визуализирует функции принадлежности
    """
    clear_screen()
    print("=== Визуализация функций принадлежности ===")
    
    fuzzy_system = FuzzyGradeSystem()
    fig = fuzzy_system.visualize()
    plt.show()
    
    input("\nНажмите Enter для продолжения...")

def show_history():
    """
    Отображает историю оценок
    """
    clear_screen()
    print("=== История оценок ===")
    
    # Загрузка данных
    json_results = load_results_json()
    
    if not json_results:
        print("История оценок пуста.")
    else:
        # Вывод результатов
        for i, result in enumerate(json_results, 1):
            print(f"\n{i}. Дата: {result['дата']}")
            print(f"   Студент: {result['студент']}")
            print(f"   Параметры: качество={result['параметры']['качество']}, "
                  f"точность={result['параметры']['точность']}, "
                  f"сроки={result['параметры']['сроки']}")
            print(f"   Оценка: {result['оценка']['числовая']:.2f} ({result['оценка']['текстовая']})")
    
    input("\nНажмите Enter для продолжения...")

def run_tests():
    """
    Запускает тестовые сценарии и выводит результаты
    """
    clear_screen()
    print("=== Тестирование системы ===")
    
    # Тестовые данные
    test_data = [
        {"name": "Тест 1", "quality": 9, "accuracy": 9, "deadline": 10, "expected": "отличник"},
        {"name": "Тест 2", "quality": 6, "accuracy": 6, "deadline": 6, "expected": "хорошист"},
        {"name": "Тест 3", "quality": 3, "accuracy": 3, "deadline": 2, "expected": "троечник"},
        {"name": "Тест 4", "quality": 5, "accuracy": 4, "deadline": 8, "expected": "хорошист"},
        {"name": "Тест 5", "quality": 1, "accuracy": 2, "deadline": 1, "expected": "троечник"}
    ]
    
    # Создание объекта системы
    fuzzy_system = FuzzyGradeSystem()
    
    # Проведение тестов
    for test in test_data:
        numeric_grade, text_grade = fuzzy_system.evaluate(test["quality"], test["accuracy"], test["deadline"])
        
        # Определение результата теста
        test_result = "ПРОЙДЕН" if text_grade == test["expected"] else "НЕ ПРОЙДЕН"
        
        # Вывод результата
        print(f"\n{test['name']}:")
        print(f"  Параметры: качество={test['quality']}, "
              f"точность={test['accuracy']}, "
              f"сроки={test['deadline']}")
        print(f"  Ожидаемый результат: {test['expected']}")
        print(f"  Полученный результат: {text_grade} ({numeric_grade:.2f})")
        print(f"  Статус теста: {test_result}")
    
    input("\nНажмите Enter для продолжения...")

def main_menu():
    """
    Отображает главное меню программы и обрабатывает выбор пользователя
    """
    while True:
        clear_screen()
        print("=== Система оценки знаний студентов ===")
        print("1. Оценить знания студента")
        print("2. Визуализировать функции принадлежности")
        print("3. Показать историю оценок")
        print("4. Запустить тесты")
        print("0. Выход")
        
        choice = input("\nВыберите действие: ")
        
        if choice == "1":
            evaluate_student()
        elif choice == "2":
            visualize_functions()
        elif choice == "3":
            show_history()
        elif choice == "4":
            run_tests()
        elif choice == "0":
            print("Программа завершена.")
            sys.exit(0)
        else:
            print("Неверный выбор. Попробуйте снова.")
            input("Нажмите Enter для продолжения...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
        sys.exit(0)
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
        sys.exit(1) 