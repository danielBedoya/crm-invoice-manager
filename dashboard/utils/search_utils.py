def filter_data(data, q):
    q_lower = q.lower()
    return [item for item in data if
            q_lower in str(item.get("Nombres", "")).lower() or
            q_lower in str(item.get("Apellidos", "")).lower() or
            q_lower in str(item.get("Número de documento", "")).lower() or
            q_lower in str(item.get("Placa del auto", "")).lower()]
