# Signature Module Standalone (Flask)

Microproyecto aislado para actualizar firmas de Gmail por lote desde un Excel.

## Incluye
- Endpoint web `GET/POST /signatures`
- Carga de Excel (`.xlsx`) con pandas
- Actualización de firmas vía Gmail API (`users.settings.sendAs.patch`)
- Dos plantillas de firma:
  - `app/templates/template.html` (con móvil)
  - `app/templates/template2.html` (sin móvil)

## Requisitos
- Python 3.10+
- Service Account con Domain Wide Delegation
- Scope autorizado en Google Workspace:
  - `https://www.googleapis.com/auth/gmail.settings.basic`

## Instalación
1. Crear entorno virtual e instalar dependencias:
   - `pip install -r requirements.txt`
2. Configurar variables de entorno copiando `.env.example`.
3. Colocar credenciales en `data/credentials.json`.
4. Ejecutar:
   - `python run.py`

## Formato esperado del Excel
Columnas mínimas recomendadas:
- `email`
- `full_name`
- `job_title`
- `field`
- `telefono`
- `telefono_movil` (opcional)

Si `telefono_movil` está vacío, usa `template2.html`; si tiene valor, usa `template.html`.

## Migración desde tu proyecto actual
Si quieres mantener diseño exacto de firma:
1. Copia el contenido de:
   - `password-manager-flask/app/templates/template.html`
   - `password-manager-flask/app/templates/template2.html`
2. Pégalo en este proyecto, reemplazando los archivos actuales.

## Notas
- Este proyecto no incluye autenticación ni paneles del CRM.
- Mantén `data/credentials.json` fuera del control de versiones.
