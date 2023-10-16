from flask_wtf import FlaskForm
from wtforms import DateTimeLocalField


class DeviceSearchForm(FlaskForm):
    start_time = DateTimeLocalField("start_time")
    end_time = DateTimeLocalField("end_time")
