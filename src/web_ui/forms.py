"""WTForms for web UI."""

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional, URL, ValidationError
import re


class ScanForm(FlaskForm):
    target = StringField(
        'Target',
        validators=[DataRequired()],
        description='Website URL (e.g., https://example.com)'
    )
    dynamic = BooleanField('Enable Dynamic Testing', default=True)
    submit = SubmitField('Start Scan')

    def validate_target(self, field):
        # Basic URL validation
        if not re.match(r'^https?://', field.data):
            field.data = 'http://' + field.data
        # Use URL validator
        validator = URL()
        try:
            validator(self, field)
        except ValidationError:
            raise ValidationError('Invalid URL')