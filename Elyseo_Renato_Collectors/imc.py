
def calc_imc(peso, altura):
    return round( peso / (altura * altura), 2)

@app.route('/imc', methods=['POST'])
def imc():
    
    params = json.loads(request.data)
    print("params",params)
    
    peso = float(params['peso'])
    altura = float(params['altura'])
    print(peso)
    print(altura)
    
    cimc = calc_imc(peso, altura)

    # # Menos do que 18,5	Abaixo do peso
    # # Entre 18,5 e 24,9	Peso normal
    # # Entre 25 e 29,9	Sobrepeso
    # # Entre 30 e 34,9	Obesidade grau 1
    # # Entre 35 e 39,9	Obesidade grau 2
    # # Mais do que 40	Obesidade grau 3

    resultado = ''
    if(cimc <= 18.5):
        resultado = 'Abaixo do Peso'
    elif(cimc <= 24.9):
        resultado = 'Peso Normal'
    elif(cimc <= 29.9):
        resultado = 'Sobrepeso'
    elif (cimc <= 34.9):
        resultado = 'Obesidade grau 1'
    elif (cimc <= 39.9):
        resultado = 'Obesidade grau 2'
    else:
        resultado = 'Obesidade grau 3'

    resp = { "peso": params['peso'], "altura": params['altura'], "imc": cimc, "rsultado": resultado }
    return jsonify(resp)


@app.route('/ping', methods=['GET'])
def pong():
    return 'pong'