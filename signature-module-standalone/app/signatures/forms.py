from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired


class SignatureForm(FlaskForm):
    excel_file = FileField("Archivo Excel", validators=[DataRequired()])
    submit = SubmitField("Actualizar firmas")
