import json

from kafka import KafkaConsumer

result = {}

consumer = KafkaConsumer(
    bootstrap_servers=["localhost:9092"],
    group_id="demo-group",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    consumer_timeout_ms=1000,
    value_deserializer=lambda m: json.loads(m.decode("ascii")),
)

consumer.subscribe("trades-orders")

try:
    for message in consumer:
        data = message.value
        print(f"Received message: {data}")  # Agregado: Imprime el mensaje recibido
        
        symbol = data["s"]
        price = data["p"]
        volume = data["v"]
        
        # Debug: Imprime los datos extraídos del mensaje
        print(f"Symbol: {symbol}, Price: {price}, Volume: {volume}")
        
        result.setdefault(
            symbol,
            {"weighted_price": 0, "total_volume": 0, "min_offset": 10000000000000000000000},
        )
        result[symbol]["weighted_price"] += price * volume
        result[symbol]["total_volume"] += volume
        result[symbol]["min_offset"] = min(result[symbol]["min_offset"], message.offset)
        print(f"Updated result: {result[symbol]}")  # Agregado: Imprime el resultado actualizado

except Exception as e:
    print(f"Error occurred while consuming messages: {e}")
finally:
    for key in result:
        weighted_average = result[key]['weighted_price'] / result[key]['total_volume']
        print(f"Weighted average price for {key}: {weighted_average}")
    consumer.close()

    