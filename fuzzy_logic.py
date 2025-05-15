import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

class FuzzyGradeSystem:
    def __init__(self):
        # Определение входных переменных
        self.quality = ctrl.Antecedent(np.arange(0, 11, 1), 'качество')
        self.accuracy = ctrl.Antecedent(np.arange(0, 11, 1), 'точность')
        self.deadline = ctrl.Antecedent(np.arange(0, 11, 1), 'сроки')
        
        # Определение выходной переменной
        self.grade = ctrl.Consequent(np.arange(0, 11, 1), 'оценка')
        
        # Определение функций принадлежности для входных переменных
        self.quality['низкое'] = fuzz.trimf(self.quality.universe, [0, 0, 5])
        self.quality['среднее'] = fuzz.trimf(self.quality.universe, [3, 5, 8])
        self.quality['высокое'] = fuzz.trimf(self.quality.universe, [6, 10, 10])
        
        self.accuracy['низкая'] = fuzz.trimf(self.accuracy.universe, [0, 0, 5])
        self.accuracy['средняя'] = fuzz.trimf(self.accuracy.universe, [3, 5, 8])
        self.accuracy['высокая'] = fuzz.trimf(self.accuracy.universe, [6, 10, 10])
        
        self.deadline['поздно'] = fuzz.trimf(self.deadline.universe, [0, 0, 5])
        self.deadline['вовремя'] = fuzz.trimf(self.deadline.universe, [3, 5, 8])
        self.deadline['досрочно'] = fuzz.trimf(self.deadline.universe, [6, 10, 10])
        
        # Определение функций принадлежности для выходной переменной
        self.grade['троечник'] = fuzz.trimf(self.grade.universe, [0, 0, 5])
        self.grade['хорошист'] = fuzz.trimf(self.grade.universe, [3, 5, 8])
        self.grade['отличник'] = fuzz.trimf(self.grade.universe, [6, 10, 10])
        
        # Определение правил нечеткого вывода
        rule1 = ctrl.Rule(
            self.quality['высокое'] & self.accuracy['высокая'] & self.deadline['досрочно'],
            self.grade['отличник']
        )
        
        rule2 = ctrl.Rule(
            self.quality['высокое'] & self.accuracy['высокая'] & self.deadline['вовремя'],
            self.grade['отличник']
        )
        
        rule3 = ctrl.Rule(
            self.quality['среднее'] & self.accuracy['средняя'] & self.deadline['вовремя'],
            self.grade['хорошист']
        )
        
        rule4 = ctrl.Rule(
            self.quality['среднее'] & self.accuracy['высокая'] & self.deadline['вовремя'],
            self.grade['хорошист']
        )
        
        rule5 = ctrl.Rule(
            self.quality['низкое'] | self.accuracy['низкая'] | self.deadline['поздно'],
            self.grade['троечник']
        )
        
        rule6 = ctrl.Rule(
            self.quality['высокое'] & self.accuracy['средняя'] & self.deadline['вовремя'],
            self.grade['хорошист']
        )
        
        rule7 = ctrl.Rule(
            self.quality['среднее'] & self.accuracy['средняя'] & self.deadline['досрочно'],
            self.grade['хорошист']
        )
        
        # Создание системы управления
        self.grade_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
        self.grading = ctrl.ControlSystemSimulation(self.grade_ctrl)
        
    def evaluate(self, quality_val, accuracy_val, deadline_val):
        """
        Оценивает знания студента на основе входных параметров
        
        :param quality_val: качество выполнения работы (0-10)
        :param accuracy_val: точность полученного результата (0-10)
        :param deadline_val: соблюдение сроков (0-10)
        :return: кортеж (числовая_оценка, текстовая_оценка)
        """
        # Установка входных значений
        self.grading.input['качество'] = quality_val
        self.grading.input['точность'] = accuracy_val
        self.grading.input['сроки'] = deadline_val
        
        # Вычисление
        try:
            self.grading.compute()
            
            # Получение числового результата
            numeric_grade = self.grading.output['оценка']
            
            # Определение текстовой оценки на основе числового результата
            if numeric_grade < 4:
                text_grade = 'троечник'
            elif numeric_grade < 7:
                text_grade = 'хорошист'
            else:
                text_grade = 'отличник'
                
            return numeric_grade, text_grade
        except:
            return None, 'ошибка вычисления'
    
    def visualize(self):
        """
        Визуализирует функции принадлежности для всех переменных
        """
        # Создание фигуры с несколькими подграфиками
        plt.figure(figsize=(12, 10))
        
        # Качество
        plt.subplot(2, 2, 1)
        self.quality.view()
        plt.title('Качество выполнения')
        plt.ylabel('Степень принадлежности')
        plt.xlabel('Оценка (0-10)')
        
        # Точность
        plt.subplot(2, 2, 2)
        self.accuracy.view()
        plt.title('Точность результата')
        plt.ylabel('Степень принадлежности')
        plt.xlabel('Оценка (0-10)')
        
        # Сроки
        plt.subplot(2, 2, 3)
        self.deadline.view()
        plt.title('Соблюдение сроков')
        plt.ylabel('Степень принадлежности')
        plt.xlabel('Оценка (0-10)')
        
        # Оценка
        plt.subplot(2, 2, 4)
        self.grade.view()
        plt.title('Итоговая оценка')
        plt.ylabel('Степень принадлежности')
        plt.xlabel('Оценка (0-10)')
        
        plt.tight_layout()
        return plt.gcf()
    
    def visualize_result(self, quality_val, accuracy_val, deadline_val):
        """
        Визуализирует результат нечеткого вывода для конкретных входных значений
        
        :param quality_val: качество выполнения работы (0-10)
        :param accuracy_val: точность полученного результата (0-10)
        :param deadline_val: соблюдение сроков (0-10)
        """
        # Установка входных значений
        self.grading.input['качество'] = quality_val
        self.grading.input['точность'] = accuracy_val
        self.grading.input['сроки'] = deadline_val
        
        # Вычисление
        self.grading.compute()
        
        # Визуализация
        plt.figure(figsize=(8, 6))
        self.grade.view(sim=self.grading)
        plt.title(f'Результат: {self.grading.output["оценка"]:.2f}')
        plt.ylabel('Степень принадлежности')
        plt.xlabel('Оценка (0-10)')
        
        return plt.gcf() 