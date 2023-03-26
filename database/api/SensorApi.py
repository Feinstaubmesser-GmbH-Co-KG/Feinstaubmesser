from database import Configuration as configuration


def get_sensor_data_by_date_type_and_value(sensor_id: int, date: str, type: str, value: str):
    old_value = value

    if value == "Höchster Wert":
        value = "MAX(" + type + ")"

    elif value == "Tiefster Wert":
        value = "MIN(" + type + ")"

    elif value == "Durchschnittlicher Wert":
        value = "AVG(" + type + ")"

    result = configuration.execute(f"SELECT {value} FROM sensor_{sensor_id} WHERE timestamp LIKE '{date}%'")

    if type == "P1":
        return get_sensor_data_by_date_type_and_value(sensor_id=sensor_id, date=date, type="P2", value=old_value), result

    else:
        return result

