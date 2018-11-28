#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, IntegerField, StringField
from wtforms.validators import DataRequired, NumberRange


class DatacenterForm(FlaskForm):
    country = StringField('Country', validators=[DataRequired(message='Country não pode ser vazio')])
    state = StringField('State', validators=[DataRequired(message='State não pode ser vazio')])
    city = StringField('City', validators=[DataRequired(message='City não pode ser vazio')])
    tier = IntegerField('Tier', validators=[DataRequired(message='Tier não pode ser vazio'), NumberRange(min=1, max=5, message='Tier deve ser um valor entre 1 e 5')])


class ClientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message='Name não pode ser vazio')])
    email = StringField('Email', validators=[DataRequired(message='Email não pode ser vazio')])
    country = StringField('Country', validators=[DataRequired(message='Country não pode ser vazio')])
    state = StringField('State', validators=[DataRequired(message='State não pode ser vazio')])
    city = StringField('City', validators=[DataRequired(message='City não pode ser vazio')])
    zipcode = StringField('ZipCode', validators=[DataRequired(message='ZipCode não pode ser vazio')])
    street = StringField('Street', validators=[DataRequired(message='Street não pode ser vazio')])
    adnumber = IntegerField('AdNumber', validators=[DataRequired(message='AdNumber não pode ser vazio e deve ser um número inteiro')])


class StaffForm(FlaskForm):
    ssn = StringField('SSN', validators=[DataRequired(message='SSN não pode ser vazio')])
    name = StringField('Name', validators=[DataRequired(message='Name não pode ser vazio')])
    email = StringField('Email', validators=[DataRequired(message='Email não pode ser vazio')])
    role = StringField('Role', validators=[DataRequired(message='Role não pode ser vazio')])
    joindate = DateField('JoinDate', format='%d/%m/%Y', validators=[DataRequired(message='JoinDate não pode ser vazio e deve ser no formato "\%d/\%m/\%Y"')])
    remuneration = DecimalField('Remuneration', validators=[DataRequired(message='Remuneration não pode ser vazio e deve ser um número decimal')])
