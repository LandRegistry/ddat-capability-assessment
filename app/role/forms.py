from flask_wtf import FlaskForm
from wtforms import SelectField, StringField
from wtforms.validators import InputRequired, Optional


class RoleForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(message="Enter a title")])


class RoleFilterForm(FlaskForm):
    query = StringField("Search", validators=[Optional()])
    sort = SelectField(
        "Sort by",
        validators=[InputRequired()],
        choices=[("created_at", "Most recent"), ("title", "Title")],
        default="created_at",
    )
    per_page = SelectField(
        "Items per page",
        validators=[InputRequired()],
        choices=[(10, "10"), (20, "20"), (40, "40")],
        default=20,
    )


class RoleDeleteForm(FlaskForm):
    pass
