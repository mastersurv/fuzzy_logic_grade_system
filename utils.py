import json
import csv
import os
from datetime import datetime

def save_result_json(student_name, quality, accuracy, deadline, numeric_grade, text_grade, filename='results.json'):
    """
    Сохраняет результат оценки в JSON файл
    
    :param student_name: имя студента
    :param quality: качество выполнения работы (0-10)
    :param accuracy: точность полученного результата (0-10)
    :param deadline: соблюдение сроков (0-10)
    :param numeric_grade: числовая оценка
    :param text_grade: текстовая оценка (троечник/хорошист/отличник)
    :param filename: имя файла для сохранения
    """
    # Создаем запись с результатом
    result = {
        'дата': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'студент': student_name,
        'параметры': {
            'качество': quality,
            'точность': accuracy,
            'сроки': deadline
        },
        'оценка': {
            'числовая': float(numeric_grade) if numeric_grade is not None else None,
            'текстовая': text_grade
        }
    }
    
    # Проверяем, существует ли файл
    if os.path.exists(filename):
        # Если файл существует, загружаем данные
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        # Если файл не существует, создаем новый список
        data = []
    
    # Добавляем новый результат
    data.append(result)
    
    # Сохраняем данные в файл
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    return True

def save_result_csv(student_name, quality, accuracy, deadline, numeric_grade, text_grade, filename='results.csv'):
    """
    Сохраняет результат оценки в CSV файл
    
    :param student_name: имя студента
    :param quality: качество выполнения работы (0-10)
    :param accuracy: точность полученного результата (0-10)
    :param deadline: соблюдение сроков (0-10)
    :param numeric_grade: числовая оценка
    :param text_grade: текстовая оценка (троечник/хорошист/отличник)
    :param filename: имя файла для сохранения
    """
    # Создаем запись с результатом
    row = [
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        student_name,
        quality,
        accuracy,
        deadline,
        float(numeric_grade) if numeric_grade is not None else 'N/A',
        text_grade
    ]
    
    # Проверяем, существует ли файл
    file_exists = os.path.exists(filename)
    
    # Открываем файл для записи
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Если файл не существует, записываем заголовки
        if not file_exists:
            writer.writerow(['Дата', 'Студент', 'Качество', 'Точность', 'Сроки', 'Числовая оценка', 'Текстовая оценка'])
        
        # Записываем данные
        writer.writerow(row)
    
    return True

def load_results_json(filename='results.json'):
    """
    Загружает все результаты из JSON файла
    
    :param filename: имя файла для загрузки
    :return: список результатов
    """
    if not os.path.exists(filename):
        return []
    
    with open(filename, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            return data
        except json.JSONDecodeError:
            return []

def load_results_csv(filename='results.csv'):
    """
    Загружает все результаты из CSV файла
    
    :param filename: имя файла для загрузки
    :return: список результатов (словарей)
    """
    if not os.path.exists(filename):
        return []
    
    results = []
    
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)  # Считываем заголовки
        
        for row in reader:
            if len(row) >= 7:  # Проверяем, что в строке достаточно данных
                result = {
                    'дата': row[0],
                    'студент': row[1],
                    'параметры': {
                        'качество': float(row[2]),
                        'точность': float(row[3]),
                        'сроки': float(row[4])
                    },
                    'оценка': {
                        'числовая': float(row[5]) if row[5] != 'N/A' else None,
                        'текстовая': row[6]
                    }
                }
                results.append(result)
    
    return results 