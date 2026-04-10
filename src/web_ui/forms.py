"""WTForms for web UI."""

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional, URL, ValidationError
import re


class ScanForm(FlaskForm):
    scan_type = SelectField(
        'Target Type',
        choices=[('local', 'Local Folder'), ('url', 'Website URL')],
        validators=[DataRequired()]
    )
    target = StringField(
        'Target',
        validators=[DataRequired()],
        description='Local folder path or website URL (e.g., https://example.com)'
    )
    dynamic = BooleanField('Enable Dynamic Testing', default=True)
    submit = SubmitField('Start Scan')

    def validate_target(self, field):
        if self.scan_type.data == 'local':
            # Local path validation: allow absolute or relative, but we check existence later
            pass
        else:  # url
            # Basic URL validation
            if not re.match(r'^https?://', field.data):
                field.data = 'http://' + field.data
            # Use URL validator
            validator = URL()
            try:
                validator(field)
            except ValidationError:
                raise ValidationError('Invalid URL')