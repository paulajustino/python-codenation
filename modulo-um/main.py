from datetime import datetime, timedelta

START_TIME = 6
END_TIME = 22
MINUTE = 0
PERMANENT_FEE = 0.36
FEE_PER_MINUTE = 0.09

records = [
    {'source': '48-996355555', 'destination': '48-666666666',
        'end': 1564610974, 'start': 1564610674},
    {'source': '41-885633788', 'destination': '41-886383097',
        'end': 1564506121, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-886383097',
        'end': 1564630198, 'start': 1564629838},
    {'source': '48-999999999', 'destination': '41-885633788',
        'end': 1564697158, 'start': 1564696258},
    {'source': '41-833333333', 'destination': '41-885633788',
        'end': 1564707276, 'start': 1564704317},
    {'source': '41-886383097', 'destination': '48-996384099',
        'end': 1564505621, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '48-996383697',
        'end': 1564505721, 'start': 1564504821},
    {'source': '41-885633788', 'destination': '48-996384099',
        'end': 1564505721, 'start': 1564504821},
    {'source': '48-996355555', 'destination': '48-996383697',
        'end': 1564505821, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '41-886383097',
        'end': 1564610750, 'start': 1564610150},
    {'source': '48-996383697', 'destination': '41-885633788',
        'end': 1564505021, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-885633788',
        'end': 1564627800, 'start': 1564626000}
]


def classify_by_phone_number(records):
    # ordenar lista de chamadas a partir de numero de origem
    # para facilitar busca e calculo
    records.sort(key=lambda k: k['source'])

    # percorre lista enquanto calcula tarifa
    # e agrega informacoes na lista de resultados
    result = []
    current_call_source = ''
    for call in records:
        if current_call_source != call['source']:
            current_call = {'source': '', 'total': 0.0}
            current_call['source'] = call['source']
            current_call['total'] = calculate_fare(call)
            current_call_source = call['source']
            result.append(current_call)
        else:
            current_call['total'] += calculate_fare(call)

        current_call['total'] = round(current_call['total'], 2)

    # retorna lista ordenada pelo maior valor total de tarifacao
    # entre os numeros de origem
    return sorted(result, key=lambda result: result['total'], reverse=True)


def calculate_fare(call):
    fare = 0
    total_minutes = 0
    initial_time = datetime.fromtimestamp(call['start'])
    final_time = datetime.fromtimestamp(call['end'])

    end_duration = timedelta(hours=final_time.hour, minutes=final_time.minute)
    start_duration = timedelta(hours=initial_time.hour, minutes=initial_time.minute)

    # calcula tarifacao de acordo com tabela de valores
    if START_TIME <= initial_time.hour < END_TIME:
        if final_time.hour >= END_TIME:
            final_time.hour = END_TIME
            final_time.minute = MINUTE

        total_minutes = (end_duration - start_duration).total_seconds() // 60
    elif START_TIME <= final_time.hour < END_TIME:
        if initial_time.hour < START_TIME:
            initial_time.hour = START_TIME
            initial_time.minute = MINUTE

        total_minutes = (end_duration - start_duration).total_seconds() // 60

    if initial_time.second > final_time.second:
        total_minutes -= 1

    fare = (total_minutes * FEE_PER_MINUTE) + PERMANENT_FEE
    return fare
