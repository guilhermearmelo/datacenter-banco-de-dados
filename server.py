#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

try:
    import pip
except:
    import urllib
    urllib.urlretrieve("https://bootstrap.pypa.io/get-pip.py", "get-pip.py")
    import os
    os.system('python get-pip.py --user')
    import pip

pip.main(['install', '--upgrade', '--user', 'flask', 'Flask-WTF'])


class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)


sys.stdout = Unbuffered(sys.stdout)

import logging, os, re
from flask import flash, Flask, redirect, render_template, request, url_for
from database import *
from forms import *

app = Flask(__name__)
app.secret_key = '4a4d443679ed46f7514ad6dbe3733c3d'
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
stdouthandler = logging.StreamHandler(sys.stdout)
stdouthandler.setFormatter(logging.Formatter(
    u'%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]\n')
)
app.logger.addHandler(stdouthandler)
app.logger.setLevel(logging.DEBUG)
filehandler = logging.FileHandler('server.out')
filehandler.setFormatter(logging.Formatter(
    u'%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]\n')
)
app.logger.addHandler(filehandler)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('template.html')


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Erro no campo %s - %s" % (getattr(form, field).label.text, error))


@app.route('/insert/datacenter', methods=['GET', 'POST'])
def insert_datacenter():
    form = DatacenterForm()
    if form.validate_on_submit():
        sql_query = 'INSERT INTO datacenter ("Country", "State", "City", "Tier") '
        sql_query += 'VALUES ("{}", "{}", "{}", "{}");'.format(
            form.country.data, form.state.data, form.city.data, form.tier.data)
        app.logger.debug('built sql: ' + str(sql_query))
        sql(sql_query)
        return redirect(url_for('query', table='datacenter'), code=307)

    flash_errors(form)
    return render_template('insert_datacenter.html', form=form)


@app.route('/insert/client', methods=['GET', 'POST'])
def insert_client():
    form = ClientForm()
    if form.validate_on_submit():
        sql_query = 'INSERT INTO client ("Name", "Email", "Country", "State", "City", "ZipCode", "Street", "AdNumber") '
        sql_query += 'VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");'.format(
            form.name.data, form.email.data, form.country.data, form.state.data,
            form.city.data, form.zipcode.data, form.street.data, form.adnumber.data)
        app.logger.debug('built sql: ' + str(sql_query))
        sql(sql_query)
        return redirect(url_for('query', table='client'), code=307)

    flash_errors(form)
    return render_template('insert_client.html', form=form)


@app.route('/insert/staff', methods=['GET', 'POST'])
def insert_staff():
    form = StaffForm()
    if form.validate_on_submit():
        sql_query = 'INSERT INTO staff ("SSN", "Name", "Email", "Role", "JoinDate", "Remuneration") '
        sql_query += 'VALUES ("{}", "{}", "{}", "{}", "{}", "{}");'.format(
            form.ssn.data, form.name.data, form.email.data, form.role.data,
            form.joindate.data.strftime('%d/%m/%Y'), form.remuneration.data)
        app.logger.debug('built sql: ' + str(sql_query))
        sql(sql_query)
        return redirect(url_for('query', table='staff'), code=307)

    flash_errors(form)
    return render_template('insert_staff.html', form=form)


@app.route('/query/<table>', methods=['GET', 'POST'])
def query(table='free'):
    app.logger.debug(str(table))
    if request.method == 'POST':
        query_table = None
        query = request.form.get('query', None)
        app.logger.debug('query: '+str(query))
        column = request.form.get('column', None)
        app.logger.debug('column: '+str(column))
        option = request.form.get('option', None)
        app.logger.debug('option: '+str(option))
        sql_query = 'SELECT * FROM '+str(table)+' WHERE '+str(column)

        if option == 'like':
            sql_query += ' LIKE \'%%'+str(query)+'%%\';'
        else:
            sql_query += ' = '+str(query)+';'

        if request.form.get('request_type', '') == 'query_all' or not query:
            sql_query = 'SELECT * FROM '+str(table)+';'
            query_table = table
        elif request.form.get('request_type', '') == 'query_free':
            sql_query = str(query)+';'
            found = re.search('FROM (.*)', query, re.IGNORECASE)
            if found:
                query_table = found.group(1)
            else:
                query_table = table
        else:
            query_table = table

        app.logger.debug('built sql: '+str(sql_query))
        elements = sql(sql_query)
        app.logger.debug('elements: '+str(elements))
        elements = [list(elem) for elem in elements]
        app.logger.debug('elements: '+str(elements))
        converted_elements = []
        for list_of_elements in elements:
            converted_elements.append([str(item) for item in list_of_elements])
        app.logger.debug('elements: '+str(converted_elements))
        elements = converted_elements
        if elements:
            return render_template(str(table)+'s_table.html', elements=elements, table=query_table)
    return render_template(str(table)+'s_table.html')


@app.route('/delete/<table>/<element_id>', methods=['GET', 'POST'])
def delete(table=None, element_id=None):
    app.logger.debug(str(table))
    app.logger.debug('Tentativa de remocao na tabela '+str(table)+' de elemento com id '+str(element_id))
    if table and element_id:
        query = 'DELETE FROM '+table+' WHERE '+table+'_id='+element_id+';'
        sql(query)
        msg = 'Remocao ocorreu com sucesso'
        app.logger.info('Remocao ocorreu com sucesso')
        app.logger.info('Query realizada: '+query)
    else:
        msg ='Nao foi especificado um item corretamente, remocao nao possivel'
        app.logger.info('Nao foi especificado um item corretamente, remocao nao possivel')
    return render_template('frees_table.html', msg=msg)


if __name__ == '__main__':
    SERVER_PORT = 5000
    if not os.path.isfile(DATABASE):
        app.logger.info('Banco de dados inexistente, criando um novo com entradas default')
        init_database()
    app.logger.info('Server vai rodar na porta ' + str(SERVER_PORT))
    app.run(host='0.0.0.0', port=SERVER_PORT, threaded=True, debug=True)
