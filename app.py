from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)


db_config = {
    'host': 'localhost',
    'user': 'root',            
    'password': '12345678',    
    'database': 'granjero'
}

MAX = 10  

def get_db():
    """Abre y devuelve una conexión a MySQL."""
    return mysql.connector.connect(**db_config)

@app.route('/')
def inicio():
    return 'Servidor funcionando correctamente'

@app.route('/comprar-choclo', methods=['GET'])
def comprar_choclo():

    cliente = request.args.get('cliente')
    if not cliente:
        return jsonify({'error': 'Falta parámetro cliente'}), 400

  
    cantidad = request.args.get('cantidad', default=1, type=int)
    if cantidad < 1:
        return jsonify({
            'error': 'Cantidad inválida',
            'mensaje': 'La cantidad debe ser ≥1'
        }), 400

    ahora = datetime.now()
    ventana = ahora - timedelta(minutes=1)

    db     = get_db()
    cursor = db.cursor()

    
    cursor.execute(
        "SELECT cantidad, tiempo FROM compras WHERE cliente = %s",
        (cliente,)
    )
    fila = cursor.fetchone()

    if fila:
        cant_actual, tiempo_ant = fila
        
        if tiempo_ant < ventana:
            cant_actual = 0
    else:
        cant_actual = 0


    if cant_actual + cantidad > MAX:
        restantes = MAX - cant_actual
        cursor.close()
        db.close()
        return jsonify({
            'error': 'Rate limit excedido',
            'mensaje': f'Solo puedes comprar {restantes} choclos más este minuto',
            'cliente': cliente,
            'comprasRealizadas': cant_actual,
            'comprasRestantes': restantes
        }), 429

    nuevo_total = cant_actual + cantidad

  
    if fila:
        cursor.execute(
            "UPDATE compras SET cantidad = %s, tiempo = %s WHERE cliente = %s",
            (nuevo_total, ahora, cliente)
        )
    else:
        cursor.execute(
            "INSERT INTO compras (cliente, cantidad, tiempo) VALUES (%s, %s, %s)",
            (cliente, nuevo_total, ahora)
        )

    db.commit()
    cursor.close()
    db.close()

    
    restantes = MAX - nuevo_total
    return jsonify({
        'mensaje': f'¡{cantidad} choclos comprados exitosamente!',
        'cliente': cliente,
        'comprasRealizadas': nuevo_total,
        'comprasRestantes': restantes
    }), 200

if __name__ == '__main__':
    app.run(debug=True)