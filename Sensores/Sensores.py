import serial
import pika
import statistics
import json

# Configuración del puerto serie (serial)
port = 'COM3'  # Cambia esto al puerto correcto donde está conectado tu Arduino
baudrate = 9600

# Configuración de RabbitMQ
rabbitmq_host = 'localhost'  
rabbitmq_queue = 'datos_sensor'

# Conexión al puerto serie (serial)
ser = serial.Serial(port, baudrate)

# Conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()
channel.queue_declare(queue=rabbitmq_queue)

# Listas para almacenar los datos de los sensores
data = []
ph_data = []

# Bucle principal
while True:
    # Lectura de datos desde el puerto serie (serial)
    line = ser.readline().decode().strip()

    # Parseo de los datos
    try:
        value = float(line)  # Suponemos que los datos son números decimales
        if line.startswith('Tasa de flujo de agua'):
            data.append(value)
        elif line.startswith('Valor de pH'):
            ph_data.append(value)
    except ValueError:
        print('Valor inválido recibido:', line)

    # Realizar operaciones con los datos
    if len(data) > 0:
        # Cálculo de la media, moda y desviación estándar de la tasa de flujo de agua
        flow_mean = statistics.mean(data)
        flow_mode = statistics.mode(data)
        flow_stdev = statistics.stdev(data)

        print('Tasa de flujo de agua (media):', flow_mean)
        print('Tasa de flujo de agua (moda):', flow_mode)
        print('Tasa de flujo de agua (desviación estándar):', flow_stdev)

        # Creación del diccionario con los datos de la tasa de flujo de agua
        flow_data_dict = {
            'media_flujo_agua': flow_mean,
            'moda_flujo_agua': flow_mode,
            'desviacion_estandar_flujo_agua': flow_stdev
        }

        # Convertir el diccionario a JSON
        flow_json_data = json.dumps(flow_data_dict)

        # Envío de los datos de la tasa de flujo de agua a RabbitMQ
        channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=flow_json_data)
        print('Datos de tasa de flujo de agua enviados correctamente a RabbitMQ.')

    if len(ph_data) > 0:
        # Cálculo de la media, moda y desviación estándar del pH
        ph_mean = statistics.mean(ph_data)
        ph_mode = statistics.mode(ph_data)
        ph_stdev = statistics.stdev(ph_data)

        print('Valor de pH (media):', ph_mean)
        print('Valor de pH (moda):', ph_mode)
        print('Valor de pH (desviación estándar):', ph_stdev)

        # Creación del diccionario con los datos del pH
        ph_data_dict = {
            'media_ph': ph_mean,
            'moda_ph': ph_mode,
            'desviacion_estandar_ph': ph_stdev
        }

        # Convertir el diccionario a JSON
        ph_json_data = json.dumps(ph_data_dict)

        # Envío de los datos del pH a RabbitMQ
        channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=ph_json_data)
        print('Datos de pH enviados correctamente a RabbitMQ.')

# Cierre de conexiones
ser.close()
connection.close()
