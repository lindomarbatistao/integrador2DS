from django.shortcuts import render
from django.http import HttpResponse
from .forms import CSVUploadForm, CSVUploadTemp
from .models import Sensor

import csv 
from datetime import datetime 
from dateutil import parser
import pytz 
import os 
import django
from app_smart.models import TemperaturaData, Sensor 


def abre_index(request):
    mensagem = "OLÁ TURMA, SEJAM FELIZES SEMPRE!"
    return HttpResponse(mensagem)


def upload_csv_view(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            csv_file = request.FILES['file']
            
            # Verifica se o arquivo tem a extensão correta
            if not csv_file.name.endswith('.csv'):
                form.add_error('file', 'Este não é um arquivo CSV válido.')
            else:
                # Processa o arquivo CSV
                file_data = csv_file.read().decode('ISO-8859-1').splitlines()
                reader = csv.DictReader(file_data, delimiter=',')  # Altere para ',' se necessário
                
                for row in reader:
                    try:
                        Sensor.objects.create(
                            tipo=row['tipo'],
                            unidade_medida=row['unidade_medida'] if row['unidade_medida'] else None,
                            latitude=float(row['latitude'].replace(',', '.')),
                            longitude=float(row['longitude'].replace(',', '.')),
                            localizacao=row['localizacao'],
                            responsavel=row['responsavel'] if row['responsavel'] else '',
                            status_operacional=True if row['status_operacional'] == 'True' else False,
                            observacao=row['observacao'] if row['observacao'] else '',
                            mac_address=row['mac_address'] if row['mac_address'] else None
                        )
                    except KeyError as e:
                        print(f"Chave não encontrada: {e} na linha: {row}")  # Exibe o erro e a linha problemática
                

    else:
        form = CSVUploadForm()

    return render(request, 'app_smart/upload_csv.html', {'form': form})


def load_temperature_data(request):
    if request.method == 'POST':
        form = CSVUploadTemp(request.POST, request.FILES)
        
        if form.is_valid():
            csv_file = request.FILES['file']
            
            # Verifica se o arquivo tem a extensão correta
            if not csv_file.name.endswith('.csv'):
                form.add_error('file', 'Este não é um arquivo CSV válido.')
            else:
                # Processa o arquivo CSV
                file_data = csv_file.read().decode('ISO-8859-1').splitlines()
                reader = csv.DictReader(file_data, delimiter=',')  # Altere para ',' se necessário
                
                for row in reader:
                    try:
                        sensor_id = int(row['sensor_id'])             
                        valor = float(row['valor'])
                        timestamp = parser.parse(row['timestamp'])  

                        try:
                            sensor_instance = Sensor.objects.get(id=sensor_id)
                        except Sensor.DoesNotExist:
                            print(f"Sensor com ID {sensor_id} não encontrado. Pulando a linha: {row}")
                            continue  # Pule para a próxima iteração se o sensor não existir
                        
                        TemperaturaData.objects.create(
                            sensor=sensor_instance,  # Atribuindo a instância do Sensor
                            valor=valor, 
                            timestamp=timestamp
                        )    
                    except KeyError as e:
                        print(f"Chave não encontrada: {e} na linha: {row}")  # Exibe o erro e a linha problemática
                

    else:
        form = CSVUploadTemp()

    return render(request, 'app_smart/upload_csv.html', {'form': form})





# Configuração do Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_city.settings') 
# django.setup()

# def load_temperature_data(csv_file_path):     
#     print("Início da importação:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))     
#     with open(csv_file_path, newline='', encoding='utf-8') as csvfile:         
#         reader = csv.DictReader(csvfile)         
#         line_count = 0         
#         for row in reader:             
#             sensor_id = int(row['sensor_id'])             
#             valor = float(row['valor'])
#             timestamp = parser.parse(row['timestamp'])  
#             # Usa dateutil para analisar a data com fuso horário
#             sensor = Sensor.objects.get(id=sensor_id)
#             TemperaturaData.objects.create(sensor=sensor, valor=valor, timestamp=timestamp)             
#             line_count += 1             
#             if line_count % 10000 == 0:                 
#                 print(f"{line_count} linhas processadas...")
#     print("Fim da importação:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#     print(f"Dados carregados com sucesso de {csv_file_path}")
# # Chame a função para carregar os dados do arquivo CSV 
# load_temperature_data('dados/temperatura_data.csv')