from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Funções para manipular arquivos
def ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as file:
            linhas = file.readlines()
        return [tuple(linha.strip().split(',')) for linha in linhas]
    except FileNotFoundError:
        return []

def salvar_arquivo(nome_arquivo, dados):
    with open(nome_arquivo, 'w', encoding='utf-8') as file:
        for linha in dados:
            file.write(','.join(map(str, linha)) + '\n')

# Inicializar os dados dos arquivos
paises = ler_arquivo('paises.txt')  # Ex.: [(1, 'Brasil'), (2, 'Argentina')]
times = ler_arquivo('times.txt')  # Ex.: [(1, 'Brasil', 'Flamengo')]
titulos = ler_arquivo('titulos.txt')  # Ex.: [(2023, 'T1')]
jogadores = ler_arquivo('jogadores.txt')  # Ex.: [('Neymar', 2023)]

@app.route('/')
def index():
    return render_template('index.html', paises=paises, times=times, titulos=titulos, jogadores=jogadores)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':

         # Adicionar País
        if 'pais' in request.form:
            novo_pais = request.form['pais'].strip()
            # Criando o ID do país no formato incremental (1, 2, 3...)
            id_pais = len(paises) + 1
            paises.append((id_pais, novo_pais))  # ID, Nome do País
            salvar_arquivo('paises.txt', paises)
        
        # Adicionar Time
        if 'time' in request.form and 'pais_id_time' in request.form:
            novo_time = request.form['time'].strip()
            pais_id_time = int(request.form['pais_id_time'])
            # Criando o ID do time no formato T1, T2, T3...
            id_time = f'T{len(times) + 1}'  # ID do time com o formato 'T1', 'T2', 'T3', etc.
            times.append((id_time, pais_id_time, novo_time))  # ID, País, Nome
            salvar_arquivo('times.txt', times)

        # Adicionar Título
        elif 'ano_titulo' in request.form and 'time_id_titulo' in request.form:
            ano_titulo = request.form['ano_titulo'].strip()
            time_id_titulo = request.form['time_id_titulo']
            titulos.append((ano_titulo, time_id_titulo))  # Ano, Time ID
            salvar_arquivo('titulos.txt', titulos)

        # Adicionar Jogador
        elif 'jogador' in request.form and 'ano_jogador' in request.form:
            nome_jogador = request.form['jogador'].strip()
            ano_jogador = int(request.form['ano_jogador'])
            jogadores.append((nome_jogador, ano_jogador))  # Nome, Ano do Título
            salvar_arquivo('jogadores.txt', jogadores)

        # Redirecionar para a página index após a adição
        return redirect(url_for('index'))

    return render_template('adicionar.html', paises=paises, times=times)

@app.route('/paises')
def listar_paises():
    return render_template('paises.html', paises=paises)

@app.route('/times')
def listar_times():
    return render_template('times.html', times=times)

@app.route('/titulos')
def listar_titulos():
    return render_template('titulos.html', titulos=titulos, times=times)

@app.route('/jogadores')
def listar_jogadores():
    return render_template('jogadores.html', jogadores=jogadores, times=times)

if __name__ == '__main__':
    app.run(debug=True)
