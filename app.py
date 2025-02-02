from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploads'
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_csv():
        if request.method == 'POST':
            file = request.files['file']
            if file and file.filename.endswith('.csv'):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                return redirect(url_for('list_clients'))
        return render_template('upload.html')

    @app.route('/clients')
    def list_clients():
        csv_files = os.listdir(app.config['UPLOAD_FOLDER'])
        if not csv_files:
            return "No CSV uploaded yet."
        df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], csv_files[0]))
        clients = df.to_dict(orient='records')
        return render_template('clients.html', clients=clients)

    @app.route('/client/<name>')
    def client_detail(name):
        csv_files = os.listdir(app.config['UPLOAD_FOLDER'])
        if not csv_files:
            return "No CSV uploaded yet."
        df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], csv_files[0]))
        client_data = df[df['Nombre del cliente'] == name].to_dict(orient='records')
        return render_template('client_detail.html', client=name, records=client_data)

    @app.route('/reports')
    def reports():
        csv_files = os.listdir(app.config['UPLOAD_FOLDER'])
        if not csv_files:
            return "No CSV uploaded yet."
        df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], csv_files[0]))
        monthly_repostajes = df.groupby('Fecha')['Cantidad de Litros'].sum().to_dict()
        return render_template('reports.html', monthly_repostajes=monthly_repostajes)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, name='RoutexApp')
