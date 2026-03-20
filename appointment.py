"""
Модуль записи на прием к врачу
ИНТЕГРИРУЕМЫЙ МОДУЛЬ - будет подключен к основному приложению

Функции модуля:
- get_doctors() - получение списка врачей
- get_available_slots() - получение свободного времени
- check_availability() - проверка доступности
- make_appointment() - создание записи
- get_appointments_by_phone() - поиск записей по телефону
- cancel_appointment() - отмена записи
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

# ============================================================
# КОНСТАНТЫ
# ============================================================

# Список врачей
DOCTORS = [
    {'id': 1, 'name': 'Иванова А.А.', 'specialty': 'Терапевт', 'schedule': '09:00-17:00'},
    {'id': 2, 'name': 'Петров Б.Б.', 'specialty': 'Педиатр', 'schedule': '09:00-15:00'},
    {'id': 3, 'name': 'Сидорова В.В.', 'specialty': 'Окулист', 'schedule': '10:00-18:00'},
    {'id': 4, 'name': 'Кузнецов Г.Г.', 'specialty': 'Лор', 'schedule': '08:00-14:00'}
]

# Доступное время для записи (все возможные слоты)
AVAILABLE_TIMES = ['09:00', '10:00', '11:00', '12:00', '14:00', '15:00', '16:00', '17:00']

# Директория для хранения данных
DATA_DIR = 'data'
APPOINTMENTS_FILE = os.path.join(DATA_DIR, 'appointments.json')


# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ (внутренние)
# ============================================================

def _ensure_data_dir():
    """Создает папку для данных, если её нет"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"[Модуль] Создана папка для данных: {DATA_DIR}")


def _load_appointments() -> List[Dict]:
    """
    Загружает все записи из JSON файла

    Returns:
        list: список записей
    """
    _ensure_data_dir()

    if not os.path.exists(APPOINTMENTS_FILE):
        # Если файла нет, создаем пустой список
        return []

    try:
        with open(APPOINTMENTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # Если файл поврежден или не найден, возвращаем пустой список
        return []


def _save_appointments(appointments: List[Dict]):
    """
    Сохраняет записи в JSON файл

    Args:
        appointments: список записей для сохранения
    """
    _ensure_data_dir()

    with open(APPOINTMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(appointments, f, ensure_ascii=False, indent=2)

    print(f"[Модуль] Сохранено {len(appointments)} записей")


# ============================================================
# ПУБЛИЧНЫЕ ФУНКЦИИ (API модуля)
# ============================================================

def get_doctors() -> List[Dict]:
    """
    Возвращает список врачей

    Returns:
        list: список врачей с полями id, name, specialty, schedule
    """
    print("[Модуль] Вызвана функция get_doctors()")
    return DOCTORS


def get_available_slots(doctor_id: int, date: str) -> List[str]:
    """
    Возвращает список свободных слотов для врача на указанную дату

    Args:
        doctor_id: ID врача
        date: дата в формате ГГГГ-ММ-ДД

    Returns:
        list: список свободного времени (например, ["09:00", "10:00"])
    """
    print(f"[Модуль] Вызвана get_available_slots(doctor_id={doctor_id}, date={date})")

    # Загружаем все записи
    appointments = _load_appointments()

    # Находим занятые слоты для указанного врача и даты
    booked_slots = [
        apt['time'] for apt in appointments
        if apt['doctor_id'] == doctor_id and apt['date'] == date
    ]

    print(f"[Модуль] Занятые слоты: {booked_slots}")

    # Вычисляем свободные слоты
    available_slots = [time for time in AVAILABLE_TIMES if time not in booked_slots]

    print(f"[Модуль] Свободные слоты: {available_slots}")

    return available_slots


def check_availability(doctor_id: int, date: str, time: str) -> bool:
    """
    Проверяет, свободно ли указанное время

    Args:
        doctor_id: ID врача
        date: дата в формате ГГГГ-ММ-ДД
        time: время в формате ЧЧ:ММ

    Returns:
        bool: True если свободно, False если занято
    """
    print(f"[Модуль] Вызвана check_availability(doctor_id={doctor_id}, date={date}, time={time})")

    available_slots = get_available_slots(doctor_id, date)
    is_available = time in available_slots

    print(f"[Модуль] Результат проверки: {is_available}")

    return is_available


def make_appointment(doctor_id: int, doctor_name: str, date: str, time: str,
                     patient_name: str, patient_phone: str) -> Dict:
    """
    Создает новую запись на прием

    Args:
        doctor_id: ID врача
        doctor_name: ФИО врача
        date: дата приема
        time: время приема
        patient_name: ФИО пациента
        patient_phone: телефон пациента

    Returns:
        dict: {'success': bool, 'ticket_number': str, 'error': str, 'appointment': dict}
    """
    print(f"[Модуль] Вызвана make_appointment()")
    print(f"[Модуль] Данные: врач={doctor_name}, дата={date}, время={time}, пациент={patient_name}")

    # Проверка доступности времени
    if not check_availability(doctor_id, date, time):
        return {
            'success': False,
            'error': 'Выбранное время уже занято'
        }

    # Проверка заполнения данных
    if not patient_name or not patient_phone:
        return {
            'success': False,
            'error': 'Заполните ФИО и телефон пациента'
        }

    # Загружаем существующие записи
    appointments = _load_appointments()

    # Генерируем новый ID
    new_id = max([apt['id'] for apt in appointments], default=0) + 1

    # Создаем запись
    new_appointment = {
        'id': new_id,
        'doctor_id': doctor_id,
        'doctor_name': doctor_name,
        'date': date,
        'time': time,
        'patient_name': patient_name,
        'patient_phone': patient_phone,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # Сохраняем
    appointments.append(new_appointment)
    _save_appointments(appointments)

    print(f"[Модуль] Запись создана, ID={new_id}, талон=ТАЛОН-{new_id}")

    return {
        'success': True,
        'ticket_number': f'ТАЛОН-{new_id}',
        'appointment': new_appointment
    }


def get_appointments_by_phone(phone: str) -> List[Dict]:
    """
    Находит все записи по номеру телефона

    Args:
        phone: номер телефона пациента

    Returns:
        list: список записей
    """
    print(f"[Модуль] Вызвана get_appointments_by_phone(phone={phone})")

    appointments = _load_appointments()

    result = [apt for apt in appointments if apt['patient_phone'] == phone]

    print(f"[Модуль] Найдено записей: {len(result)}")

    return result


def cancel_appointment(appointment_id: int) -> Dict:
    """
    Отменяет запись по ID

    Args:
        appointment_id: ID записи для отмены

    Returns:
        dict: {'success': bool, 'error': str}
    """
    print(f"[Модуль] Вызвана cancel_appointment(appointment_id={appointment_id})")

    appointments = _load_appointments()

    # Ищем запись
    for i, apt in enumerate(appointments):
        if apt['id'] == appointment_id:
            # Удаляем запись
            removed = appointments.pop(i)
            _save_appointments(appointments)

            print(f"[Модуль] Запись отменена: {removed}")

            return {'success': True}

    print(f"[Модуль] Запись с ID={appointment_id} не найдена")

    return {'success': False, 'error': 'Запись не найдена'}


# ============================================================
# ДЛЯ ТЕСТИРОВАНИЯ МОДУЛЯ
# ============================================================

if __name__ == '__main__':
    """Тестирование модуля (запуск отдельно)"""
    print("=" * 50)
    print("ТЕСТИРОВАНИЕ МОДУЛЯ appointment.py")
    print("=" * 50)

    # Тест 1: Получение списка врачей
    print("\n1. get_doctors():")
    doctors = get_doctors()
    for d in doctors:
        print(f"   - {d['specialty']} {d['name']}")

    # Тест 2: Проверка свободных слотов
    print("\n2. get_available_slots(doctor_id=1, date='2026-03-25'):")
    slots = get_available_slots(1, '2026-03-25')
    print(f"   Свободные слоты: {slots}")

    # Тест 3: Создание записи
    print("\n3. make_appointment():")
    result = make_appointment(
        doctor_id=1,
        doctor_name='Иванова А.А.',
        date='2026-03-25',
        time='10:00',
        patient_name='Иванов Иван Иванович',
        patient_phone='+79991112233'
    )
    print(f"   Результат: {result}")

    # Тест 4: Проверка, что время стало занятым
    print("\n4. Проверка доступности после записи:")
    is_available = check_availability(1, '2026-03-25', '10:00')
    print(f"   Время 10:00 доступно? {is_available}")

    print("\n" + "=" * 50)
    print("Тестирование модуля завершено")