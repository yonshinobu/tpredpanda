
import json

import websocket
from kafka import KafkaProducer

# Configura las direcciones de Kafka obtenidas de la configuración de Redpanda
bootstrap_servers = ['localhost:9092']

# Crea un productor de Kafka
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

topic = "trades-orders"

def on_message(ws, message):
    print(message)
    data = json.loads(message)
    if data['type'] == 'trade':
        # Filtra los datos para los símbolos específicos
        if data['data'][0]['s'] in ['AAPL', 'AMZN', 'BINANCE:BTCUSDT']:
            producer.send('trades-orders', value=data['data'][0])


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=cjegoihr01qgod9an6l0cjegoihr01qgod9an6lg",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
    