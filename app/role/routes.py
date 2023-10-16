import csv
from datetime import datetime
from io import StringIO

import pytz
from flask import Response, flash, redirect, render_template, request, url_for

from app import db
from app.models import Role
from app.role import bp
from app.role.forms import RoleDeleteForm, RoleFilterForm, RoleForm


@bp.route("/", methods=["GET", "POST"])
def list():
    """Get a list of Roles."""
    form = RoleFilterForm()

    page = request.args.get("page", type=int)
    per_page = request.args.get("per_page", type=int)
    search = request.args.get("query", type=str)
    sort_by = request.args.get("sort", type=str)

    query = Role.query

    if search:
        query = query.filter(Role.title.ilike(f"%{search}%"))
        form.query.data = search

    if sort_by and sort_by != "created_at":
        query = query.order_by(getattr(Role, sort_by).asc(), Role.created_at.desc())
        form.sort.data = sort_by
    else:
        query = query.order_by(Role.created_at.desc())

    if per_page:
        form.per_page.data = str(per_page)

    roles = query.paginate(page=page, per_page=per_page, max_per_page=40)

    return render_template("list_roles.html", roles=roles, form=form)


@bp.route("/new", methods=["GET", "POST"])
def create():
    """Create a new Role."""
    form = RoleForm()

    if form.validate_on_submit():
        new_role = Role(title=form.title.data.strip().title())
        db.session.add(new_role)
        db.session.commit()
        flash(
            f"{new_role.title} has been created.",
            "success",
        )
        return redirect(url_for("role.list"))

    return render_template("create_role.html", form=form)


@bp.route("/<uuid:id>/edit", methods=["GET", "POST"])
def edit(id):
    """Edit a Role with a specific ID."""
    role = Role.query.get_or_404(str(id))
    form = RoleForm()

    if form.validate_on_submit():
        role.title = form.title.data.strip().title()
        role.updated_at = pytz.utc.localize(datetime.utcnow())
        db.session.add(role)
        db.session.commit()
        flash(
            f"Your changes to <a href='{url_for('role.view', id=role.id)}' class='alert-link'>{role.title}</a> have been saved.",
            "success",
        )
        return redirect(url_for("role.list"))
    elif request.method == "GET":
        form.title.data = role.title

    return render_template(
        "edit_role.html",
        form=form,
        role=role,
    )


@bp.route("/<uuid:id>/delete", methods=["GET", "POST"])
def delete(id):
    """Delete a Role with a specific ID."""
    role = Role.query.get_or_404(str(id))
    form = RoleDeleteForm()

    if request.method == "GET":
        return render_template(
            "delete_role.html",
            form=form,
            role=role,
        )
    elif request.method == "POST":
        db.session.delete(role)
        db.session.commit()
        flash(f"{role.title} has been deleted.", "success")
        return redirect(url_for("role.list"))


@bp.route("/download", methods=["GET"])
def download():
    """Download a list of Roles."""
    search = request.args.get("query", type=str)
    sort_by = request.args.get("sort", type=str)

    query = Role.query

    if search:
        query = query.filter(Role.title.ilike(f"%{search}%"))

    if sort_by and sort_by != "created_at":
        query = query.order_by(getattr(Role, sort_by).asc(), Role.created_at.desc())
    else:
        query = query.order_by(Role.created_at.desc())

    roles = query.all()

    def generate():
        data = StringIO()
        w = csv.writer(data)

        # write header
        w.writerow(("ID", "TITLE", "CREATED_AT", "UPDATED_AT"))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        # write each item
        for role in roles:
            w.writerow(
                (
                    role.id,
                    role.title,
                    role.created_at.isoformat(),
                    role.updated_at.isoformat() if role.updated_at else None,
                )
            )
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    response = Response(generate(), mimetype="text/csv", status=200)
    response.headers.set("Content-Disposition", "attachment", filename="roles.csv")
    return response
