from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class DeviceForm(FlaskForm):
    device_ip = StringField('Device IP', validators=[DataRequired()])
    device_name = StringField('Device Name', validators=[DataRequired()])
    # submit = SubmitField('Submit')
    csrf_enabled = False  # Disable CSRF protection for this form



class GroupForm(FlaskForm):
    group_name = StringField('Group Name', validators=[DataRequired()])
    csrf_enabled = False  # Disable CSRF protection for this form
