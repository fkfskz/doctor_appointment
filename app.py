"""
Сервис записи на прием к врачу
ВЕРСИЯ С ИНТЕГРИРОВАННЫМ МОДУЛЕМ

Использует модуль appointment.py для:
- Получения списка врачей
- Проверки доступности времени
- Сохранения записей
- Поиска записей по телефону
- Отмены записей
"""

from flask import Flask, render_template, request, jsonify

# ИНТЕГРАЦИЯ МОДУЛЯ - импортируем все нужные функции
from appointment import (
    get_doctors,  # список врачей
    get_available_slots,  # свободные слоты
    check_availability,  # проверка доступности
    make_appointment,  # создание записи
    get_appointments_by_phone,  # поиск по телефону
    cancel_appointment  # отмена записи
)

app = Flask(__name__)
app.secret_key = 'secret_key_for_session'


@app.route('/')
def index():
    """
    Главная страница
    Использует интегрированный модуль для получения списка врачей
    """
    # ВЫЗОВ ИНТЕГРИРОВАННОГО МОДУЛЯ
    doctors = get_doctors()

    return render_template('index.html', doctors=doctors)


@app.route('/available_slots')
def available_slots():
    """
    API: получить свободные слоты для врача на дату
    Использует интегрированный модуль
    """
    doctor_id = request.args.get('doctor_id', type=int)
    date = request.args.get('date')

    if not doctor_id or not date:
        return jsonify({'error': 'Не указаны врач или дата'}), 400

    # ВЫЗОВ ИНТЕГРИРОВАННОГО МОДУЛЯ
    slots = get_available_slots(doctor_id, date)

    return jsonify({'slots': slots})


@app.route('/make_appointment', methods=['POST'])
def make_appointment_route():
    """
    API: создать запись на прием
    Использует интегрированный модуль
    """
    # Получаем данные из формы
    doctor_id = request.form.get('doctor_id', type=int)
    doctor_name = request.form.get('doctor_name')
    date = request.form.get('date')
    time = request.form.get('time')
    patient_name = request.form.get('patient_name')
    patient_phone = request.form.get('patient_phone')

    # Проверка обязательных полей
    if not all([doctor_id, doctor_name, date, time, patient_name, patient_phone]):
        return jsonify({
            'success': False,
            'error': 'Заполните все поля'
        })

    # ВЫЗОВ ИНТЕГРИРОВАННОГО МОДУЛЯ
    result = make_appointment(
        doctor_id=doctor_id,
        doctor_name=doctor_name,
        date=date,
        time=time,
        patient_name=patient_name,
        patient_phone=patient_phone
    )

    return jsonify(result)


@app.route('/check_appointments')
def check_appointments():
    """
    API: проверить записи по номеру телефона
    Использует интегрированный модуль
    """
    phone = request.args.get('phone')

    if not phone:
        return jsonify({'error': 'Введите номер телефона'}), 400

    # ВЫЗОВ ИНТЕГРИРОВАННОГО МОДУЛЯ
    appointments = get_appointments_by_phone(phone)

    return jsonify({'appointments': appointments})


@app.route('/cancel_appointment', methods=['POST'])
def cancel_appointment_route():
    """
    API: отменить запись
    Использует интегрированный модуль
    """
    appointment_id = request.form.get('appointment_id', type=int)

    if not appointment_id:
        return jsonify({'error': 'Не указан ID записи'}), 400

    # ВЫЗОВ ИНТЕГРИРОВАННОГО МОДУЛЯ
    result = cancel_appointment(appointment_id)

    return jsonify(result)


if __name__ == '__main__':
    print("=" * 50)
    print("Сервис записи к врачу (с интегрированным модулем)")
    print("Запуск на http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)