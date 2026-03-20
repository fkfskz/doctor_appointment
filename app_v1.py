"""
Существующее ПО - Сервис записи к врачу (ВЕРСИЯ БЕЗ МОДУЛЯ)
Работает только с захардкоженными данными, без логики записи
"""

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Захардкоженный список врачей
DOCTORS = [
    {'id': 1, 'name': 'Иванова А.А.', 'specialty': 'Терапевт', 'schedule': '09:00-17:00'},
    {'id': 2, 'name': 'Петров Б.Б.', 'specialty': 'Педиатр', 'schedule': '09:00-15:00'},
    {'id': 3, 'name': 'Сидорова В.В.', 'specialty': 'Окулист', 'schedule': '10:00-18:00'},
    {'id': 4, 'name': 'Кузнецов Г.Г.', 'specialty': 'Лор', 'schedule': '08:00-14:00'}
]

# Захардкоженный список доступного времени
AVAILABLE_TIMES = ['09:00', '10:00', '11:00', '12:00', '14:00', '15:00', '16:00', '17:00']


@app.route('/')
def index():
    """Главная страница"""
    return render_template('index_v1.html', doctors=DOCTORS)


@app.route('/get_slots')
def get_slots():
    """
    Возвращает доступное время (всегда возвращает все слоты,
    так как нет модуля проверки занятости)
    """
    request.args.get('doctor_id')
    request.args.get('date')
    
    # В существующей версии нет проверки занятости
    # Просто возвращаем все доступные слоты
    return jsonify({'slots': AVAILABLE_TIMES})


@app.route('/make_appointment', methods=['POST'])
def make_appointment():
    """
    Создает запись (без сохранения, просто имитация)
    В существующей версии нет реального сохранения
    """
    # Получаем данные из формы
    doctor_id = request.form.get('doctor_id')
    request.form.get('doctor_name')
    date = request.form.get('date')
    time = request.form.get('time')
    patient_name = request.form.get('patient_name')
    patient_phone = request.form.get('patient_phone')
    
    # Проверка на пустые поля
    if not all([doctor_id, date, time, patient_name, patient_phone]):
        return jsonify({'success': False, 'error': 'Заполните все поля'})
    
    # В существующей версии запись НЕ сохраняется
    # Просто имитируем успешную запись
    return jsonify({
        'success': True,
        'ticket_number': 'ТАЛОН-XXX (демо)',
        'message': 'ДЕМО-ВЕРСИЯ: Запись не сохранена, так как модуль еще не интегрирован'
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)