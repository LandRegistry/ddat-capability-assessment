from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import GovSelect, GovTextInput, GovSubmitInput
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Optional


class RoleForm(FlaskForm):
    title = StringField(
        "What is the title of the role?",
        validators=[InputRequired(message="Enter the role title")],
        widget=GovTextInput(),
    )
    submit = SubmitField("Create", widget=GovSubmitInput())

class RoleFilterForm(FlaskForm):
    query = StringField("Search", validators=[Optional()])
    sort = SelectField(
        "Sort by",
        choices=[("created_at", "Most recent"), ("title", "Title")],
        default="created_at",
        validators=[InputRequired()],
        widget=GovSelect(),
    )
    per_page = SelectField(
        "Items per page",
        choices=[(10, "10"), (20, "20"), (40, "40")],
        default=20,
        validators=[InputRequired()],
        widget=GovSelect(),
    )


class RoleDeleteForm(FlaskForm):
    pass
