"""
Модуль записи на прием к врачу
ИНТЕГРИРУЕМЫЙ МОДУЛЬ - с расширенной отладкой
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

# ============================================================
# КОНСТАНТЫ
# ============================================================

DOCTORS = [
    {'id': 1, 'name': 'Иванова А.А.', 'specialty': 'Терапевт', 'schedule': '09:00-17:00'},
    {'id': 2, 'name': 'Петров Б.Б.', 'specialty': 'Педиатр', 'schedule': '09:00-15:00'},
    {'id': 3, 'name': 'Сидорова В.В.', 'specialty': 'Окулист', 'schedule': '10:00-18:00'},
    {'id': 4, 'name': 'Кузнецов Г.Г.', 'specialty': 'Лор', 'schedule': '08:00-14:00'}
]

AVAILABLE_TIMES = ['09:00', '10:00', '11:00', '12:00', '14:00', '15:00', '16:00', '17:00']

DATA_DIR = 'data'
APPOINTMENTS_FILE = os.path.join(DATA_DIR, 'appointments.json')

# Флаг для включения детальной отладки
DEBUG_MODE = True


def _log(msg: str):
    """Функция для логирования отладочных сообщений"""
    if DEBUG_MODE:
        print(f"[DEBUG] {msg}")


def _ensure_data_dir():
    """Создает папку для данных, если её нет"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        _log(f"Создана папка для данных: {DATA_DIR}")


def _load_appointments() -> List[Dict]:
    """Загружает все записи из JSON файла"""
    _ensure_data_dir()

    if not os.path.exists(APPOINTMENTS_FILE):
        _log("Файл appointments.json не найден, создаем пустой список")
        return []

    try:
        with open(APPOINTMENTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            _log(f"Загружено {len(data)} записей из файла")
            return data
    except json.JSONDecodeError as e:
        _log(f"Ошибка чтения JSON: {e}")
        return []
    except Exception as e:
        _log(f"Неожиданная ошибка при загрузке: {e}")
        return []


def _save_appointments(appointments: List[Dict]):
    """Сохраняет записи в JSON файл"""
    _ensure_data_dir()

    try:
        with open(APPOINTMENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(appointments, f, ensure_ascii=False, indent=2)
        _log(f"Сохранено {len(appointments)} записей")
    except Exception as e:
        _log(f"Ошибка при сохранении: {e}")


# ============================================================
# ПУБЛИЧНЫЕ ФУНКЦИИ (API модуля)
# ============================================================

def get_doctors() -> List[Dict]:
    """Возвращает список врачей"""
    _log("=== get_doctors() вызвана ===")
    _log(f"Возвращаем {len(DOCTORS)} врачей")
    for d in DOCTORS:
        _log(f"  - {d['specialty']}: {d['name']}")
    return DOCTORS


def get_available_slots(doctor_id: int, date: str) -> List[str]:
    """
    Возвращает список свободных слотов для врача на указанную дату
    """
    _log("=" * 50)
    _log(f"=== get_available_slots() вызвана ===")
    _log(f"  doctor_id: {doctor_id} (тип: {type(doctor_id)})")
    _log(f"  date: {date}")

    # Загружаем все записи
    appointments = _load_appointments()
    _log(f"  Всего записей в базе: {len(appointments)}")

    # Находим занятые слоты
    booked_slots = []
    for apt in appointments:
        _log(f"    Проверяем запись: doctor_id={apt['doctor_id']}, date={apt['date']}, time={apt['time']}")
        if apt['doctor_id'] == doctor_id and apt['date'] == date:
            booked_slots.append(apt['time'])
            _log(f"      -> Занято! {apt['time']}")

    _log(f"  Занятые слоты: {booked_slots}")

    # Вычисляем свободные слоты
    available_slots = [time for time in AVAILABLE_TIMES if time not in booked_slots]

    _log(f"  Все возможные слоты: {AVAILABLE_TIMES}")
    _log(f"  Свободные слоты: {available_slots}")
    _log(f"  Количество свободных: {len(available_slots)}")

    return available_slots


def check_availability(doctor_id: int, date: str, time: str) -> bool:
    """
    Проверяет, свободно ли указанное время
    """
    _log("=" * 50)
    _log(f"=== check_availability() вызвана ===")
    _log(f"  doctor_id: {doctor_id}")
    _log(f"  date: {date}")
    _log(f"  time: {time}")

    available_slots = get_available_slots(doctor_id, date)
    is_available = time in available_slots

    _log(f"  Результат: {'СВОБОДНО' if is_available else 'ЗАНЯТО'}")

    return is_available


def make_appointment(doctor_id: int, doctor_name: str, date: str, time: str,
                     patient_name: str, patient_phone: str) -> Dict:
    """
    Создает новую запись на прием
    """
    _log("=" * 50)
    _log(f"=== make_appointment() вызвана ===")
    _log(f"  doctor_id: {doctor_id}")
    _log(f"  doctor_name: {doctor_name}")
    _log(f"  date: {date}")
    _log(f"  time: {time}")
    _log(f"  patient_name: {patient_name}")
    _log(f"  patient_phone: {patient_phone}")

    # Проверка доступности времени
    _log("  Шаг 1: Проверка доступности времени...")
    if not check_availability(doctor_id, date, time):
        _log("  Шаг 1: ОШИБКА - время занято")
        return {
            'success': False,
            'error': 'Выбранное время уже занято'
        }
    _log("  Шаг 1: Время свободно ✓")

    # Проверка заполнения данных
    _log("  Шаг 2: Проверка заполнения данных...")
    if not patient_name or not patient_phone:
        _log("  Шаг 2: ОШИБКА - не заполнены ФИО или телефон")
        return {
            'success': False,
            'error': 'Заполните ФИО и телефон пациента'
        }
    _log(f"  Шаг 2: Данные заполнены: {patient_name}, {patient_phone} ✓")

    # Загружаем существующие записи
    _log("  Шаг 3: Загрузка существующих записей...")
    appointments = _load_appointments()

    # Генерируем новый ID
    if appointments:
        max_id = max([apt['id'] for apt in appointments])
        new_id = max_id + 1
        _log(f"  Шаг 4: Существующие ID: {[apt['id'] for apt in appointments]}")
        _log(f"  Шаг 4: Максимальный ID: {max_id}, новый ID: {new_id}")
    else:
        new_id = 1
        _log("  Шаг 4: Нет существующих записей, новый ID: 1")

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

    _log(f"  Шаг 5: Создана запись: {new_appointment}")

    # Сохраняем
    appointments.append(new_appointment)
    _save_appointments(appointments)

    _log(f"  Шаг 6: Запись сохранена, талон: ТАЛОН-{new_id}")
    _log("=" * 50)

    return {
        'success': True,
        'ticket_number': f'ТАЛОН-{new_id}',
        'appointment': new_appointment
    }


def get_appointments_by_phone(phone: str) -> List[Dict]:
    """Находит все записи по номеру телефона"""
    _log("=" * 50)
    _log(f"=== get_appointments_by_phone() вызвана ===")
    _log(f"  phone: {phone}")

    appointments = _load_appointments()
    _log(f"  Всего записей в базе: {len(appointments)}")

    result = []
    for apt in appointments:
        _log(f"    Проверяем запись: phone={apt['patient_phone']}")
        if apt['patient_phone'] == phone:
            result.append(apt)
            _log(f"      -> СОВПАДЕНИЕ! ID={apt['id']}")

    _log(f"  Найдено записей: {len(result)}")

    return result


def cancel_appointment(appointment_id: int) -> Dict:
    """Отменяет запись по ID"""
    _log("=" * 50)
    _log(f"=== cancel_appointment() вызвана ===")
    _log(f"  appointment_id: {appointment_id}")

    appointments = _load_appointments()
    _log(f"  Всего записей до удаления: {len(appointments)}")

    for i, apt in enumerate(appointments):
        _log(f"    Проверяем запись: ID={apt['id']}")
        if apt['id'] == appointment_id:
            _log(f"      -> НАЙДЕНО! Удаляем запись: {apt}")
            removed = appointments.pop(i)
            _save_appointments(appointments)
            _log(f"  Запись удалена, осталось {len(appointments)} записей")
            return {'success': True}

    _log(f"  Запись с ID={appointment_id} не найдена")
    return {'success': False, 'error': 'Запись не найдена'}


# ============================================================
# ДЛЯ ТЕСТИРОВАНИЯ МОДУЛЯ
# ============================================================

if __name__ == '__main__':
    """Тестирование модуля (запуск отдельно)"""
    print("\n" + "=" * 60)
    print("ТЕСТИРОВАНИЕ МОДУЛЯ appointment.py")
    print("=" * 60)

    # Тест 1: Получение списка врачей
    print("\n[Тест 1] get_doctors():")
    doctors = get_doctors()
    for d in doctors:
        print(f"   - {d['specialty']} {d['name']}")

    # Тест 2: Проверка свободных слотов (без записей)
    print("\n[Тест 2] get_available_slots(doctor_id=1, date='2026-03-25'):")
    slots = get_available_slots(1, '2026-03-25')
    print(f"   Свободные слоты: {slots}")

    # Тест 3: Создание записи
    print("\n[Тест 3] make_appointment():")
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
    print("\n[Тест 4] Проверка доступности после записи:")
    is_available = check_availability(1, '2026-03-25', '10:00')
    print(f"   Время 10:00 доступно? {is_available}")

    # Тест 5: Проверка записей по телефону
    print("\n[Тест 5] get_appointments_by_phone('+79991112233'):")
    appointments = get_appointments_by_phone('+79991112233')
    for apt in appointments:
        print(f"   - ТАЛОН-{apt['id']}: {apt['date']} {apt['time']}")

    print("\n" + "=" * 60)
    print("Тестирование модуля завершено")
    print("=" * 60)