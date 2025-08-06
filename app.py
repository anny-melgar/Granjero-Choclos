from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime, timedelta


app = Flask(__name__)


db_config = {
    'host': 'localhost',
    'user': 'root',            # tu usuario de MySQL
    'password': '12345678', # tu contraseña real
    'database': 'granjero'
}

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

    db = get_db()
    cursor = db.cursor()

  
    cursor.execute(
        "SELECT tiempo FROM compras WHERE cliente = %s ORDER BY tiempo DESC LIMIT 1",
        (cliente,)
    )
    fila = cursor.fetchone()

    ahora = datetime.now()

    if fila:
        ultima = fila[0]
       
        if ahora - ultima < timedelta(minutes=1):
            cursor.close()
            db.close()
            return jsonify({
                'error': 'Rate limit excedido',
                'mensaje': 'Solo puedes comprar 1 choclo por minuto',
                'cliente': cliente
            }), 429

    
    cursor.execute(
        "INSERT INTO compras (cliente) VALUES (%s)",
        (cliente,)
    )
    db.commit()
    cursor.close()
    db.close()

    
    return jsonify({
        'mensaje': '¡Choclo comprado exitosamente!',
        'cliente': cliente
    }), 200


if __name__ == '__main__':
    app.run(debug=True)