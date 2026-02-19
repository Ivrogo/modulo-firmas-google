from pathlib import Path

import pandas as pd
from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from google.oauth2 import service_account
from googleapiclient.discovery import build

from .forms import SignatureForm

signatures_bp = Blueprint("signatures", __name__)


@signatures_bp.route("/", methods=["GET"])
def home():
    return redirect(url_for("signatures.manage_signatures"))


@signatures_bp.route("/signatures", methods=["GET", "POST"])
def manage_signatures():
    form = SignatureForm()

    if form.validate_on_submit():
        excel_file = form.excel_file.data

        try:
            dataframe = pd.read_excel(excel_file)

            template_with_mobile = _load_template("template.html")
            template_without_mobile = _load_template("template2.html")

            scopes = current_app.config["GOOGLE_SCOPES"]
            service_account_path = _resolve_service_account_path(
                current_app.config["GOOGLE_SERVICE_ACCOUNT_FILE"]
            )

            processed = 0
            skipped = 0

            for _, row in dataframe.iterrows():
                user_email = row.get("email")
                if pd.isna(user_email) or not str(user_email).strip():
                    skipped += 1
                    continue

                credentials = service_account.Credentials.from_service_account_file(
                    str(service_account_path),
                    scopes=scopes,
                    subject=str(user_email).strip(),
                )

                service = build("gmail", "v1", credentials=credentials)

                template = template_without_mobile if pd.isna(row.get("telefono_movil")) else template_with_mobile
                row_dict = {
                    key: "" if pd.isna(value) else str(value)
                    for key, value in row.items()
                }
                signature_html = template.format(**row_dict)

                body = {"signature": signature_html}

                service.users().settings().sendAs().patch(
                    userId="me",
                    sendAsEmail=str(user_email).strip(),
                    body=body,
                ).execute()

                processed += 1

            flash(
                f"Firmas actualizadas. Procesados: {processed}. Omitidos: {skipped}.",
                "success",
            )

        except Exception as error:
            flash(f"Error al procesar firmas: {error}", "danger")

        return redirect(url_for("signatures.manage_signatures"))

    return render_template("signatures.html", title="Gestionar firmas", form=form)


def _load_template(template_name: str) -> str:
    template_path = Path(current_app.root_path) / "templates" / template_name
    return template_path.read_text(encoding="utf-8")


def _resolve_service_account_path(config_value: str) -> Path:
    service_account_path = Path(config_value)
    if service_account_path.is_absolute():
        return service_account_path
    return Path(current_app.root_path).parent / service_account_path
