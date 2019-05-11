from flask import Flask, request, g, session, redirect, url_for
from sessions import RedisSessionInterface
from desenha_tela import DesenhaTela as dt
from bd import AcessoBD

dba = AcessoBD()
app = Flask(__name__)
app.session_interface = RedisSessionInterface()
draw = dt()


@app.route('/')
def index():
    return draw.render('index')


@app.route('/ver-produto')
def ver_produto():
    return draw.render('ver-produto')


@app.route('/carrinho', methods=['GET', 'POST'])
def carrinho():
    if(request.method == 'POST'):
        return "Produto adicionado"
    else:
        return draw.render('carrinho')


@app.route('/notificacao', methods=['GET', 'POST'])
def notificacao():
    return "Notificação atividada"


@app.route('/entrar', methods=['GET', 'POST'])
def entrar():
    if(g.user):
        return redirect(url_for('index'))

    if(request.method == 'POST'):
        session.pop('user', None)
        if(dba.auth_user(request.form['email'], request.form['senha'])):
            session.permanent = True
            session['user'] = request.form['email']
            return redirect(url_for('index'))
        else:
            return draw.render('login')
    else:
        return draw.render('login')


@app.route('/sair')
def sair():
    session.pop('user', None)
    return redirect(url_for('index'))


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if(g.user):
        return redirect(url_for('index'))

    if(request.method == 'POST'):
        session.pop('user', None)
        if(len(dba.select_users(email=request.form['email'])) > 0):
            if(request.form['senha'] == request.form['senha2']):
                dba.insert_user(request.form['nome'], request.form['cpf'],
                                request.form['data_nasc'],
                                request.form['telefone'],
                                request.form['endereco'],
                                request.form['email'], request.form['senha'])
            else:
                return draw.render('cadastro')
        else:
            return draw.render('cadastro')
    else:
        pass
    return draw.render('cadastro')


@app.before_request
def before_request():
    g.user = None
    if('user' in session):
        g.user = session['user']


if __name__ == '__main__':
    app.run()
