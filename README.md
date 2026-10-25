# HCM Lite — Streamlit Edition

A Python/Streamlit starter conversion of the supplied HCM Lite HTML website. It includes role-based sign-in (Admin, HR, Employee), dashboard, employee list and registration, check-in/check-out, leave requests and approvals, basic payroll drafts/finalization, announcements, company settings, departments, and password changes.

## Run on your computer

1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. Open Terminal in VS Code and run:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   streamlit run app.py
   ```

   If PowerShell blocks activation, run this in that terminal first:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
   ```

4. Streamlit opens a local browser tab. The SQLite database is created automatically as `hcm_lite.db`.

## Demo accounts

- Admin: `admin@hcm.com` / `12345678`
- HR: `hr@hcm.com` / `12345678`
- Employee: `ayesha@hcm.com` / `12345678`

Change demo passwords before entering real information. The first startup seeds demo data only when the database has no users.

## Publish on Streamlit Community Cloud

1. Create a GitHub repository and upload `app.py`, `requirements.txt`, and `README.md`.
2. Open https://share.streamlit.io/ and sign in with GitHub.
3. Choose **Create app**, select your repository/branch, and set the main file path to `app.py`.
4. Deploy and open the generated public URL.

## Important deployment and security notes

- Streamlit Community Cloud's local filesystem is not a reliable permanent database for production. This starter uses SQLite for local testing; data may be lost or not shared reliably across app restarts/instances in the cloud. Before using real employee records, migrate the database to a managed persistent database (for example, PostgreSQL), configure backups, and test access controls.
- This is a starter conversion, not a byte-for-byte recreation of the original JavaScript website. The original browser `localStorage` data does not migrate automatically.
- Payroll is deliberately basic: gross pay is calculated as 1.5 × basic salary, with no tax, attendance deduction, overtime, or statutory payroll logic. Validate local legal requirements before using payroll for actual payments.
- Demo passwords are public and intended only for testing. Change them before sharing the deployment, and do not enter real personal or salary data until authentication, persistence, and security have been reviewed.
