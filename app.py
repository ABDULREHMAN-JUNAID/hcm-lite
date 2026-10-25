import hashlib
import hmac
import os
import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st


# -------------------- APP CONFIGURATION --------------------

APP_DIR = Path(__file__).parent
DB_PATH = Path(
    os.environ.get("HCM_DB_PATH", str(APP_DIR / "hcm_lite.db"))
)

st.set_page_config(
    page_title="HCM Lite",
    page_icon="🟢",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Bricolage+Grotesque:wght@500;600;700&display=swap');

/* ========================================
   1. GLOBAL THEME
======================================== */
:root {
    color-scheme: light;
    --primary: #087F6E;
    --primary-dark: #065F52;
    --sidebar: #103B35;
    --background: #F3F6F8;
    --surface: #FFFFFF;
    --text: #172B4D;
    --muted: #60717D;
    --border: #DCE5E8;
}

.stApp {
    background: var(--background);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] .main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* ========================================
   2. TEXT AND HEADINGS
======================================== */
.stApp p,
.stApp li,
.stApp label,
.stApp .stMarkdown,
.stApp [data-testid="stCaptionContainer"] {
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4 {
    color: #123B35 !important;
    font-family: 'Bricolage Grotesque', sans-serif;
    font-weight: 700;
    letter-spacing: -0.3px;
}

.stApp h1 {
    font-size: 2.2rem;
}

.stApp h2 {
    font-size: 1.65rem;
}

.stApp h3 {
    font-size: 1.25rem;
}

.stApp [data-testid="stCaptionContainer"] {
    color: var(--muted) !important;
}

/* ========================================
   3. SIDEBAR
======================================== */
[data-testid="stSidebar"] {
    background: var(--sidebar) !important;
    border-right: 1px solid #24574F;
}

[data-testid="stSidebar"] > div {
    background: var(--sidebar) !important;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #C5DDD7 !important;
}

/* Sidebar navigation */
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 8px 10px;
    border-radius: 8px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #1B5148;
}

/* ========================================
   4. INPUTS AND DROPDOWNS
======================================== */
.stApp input,
.stApp textarea {
    background: #FFFFFF !important;
    color: #172B4D !important;
    border: 1px solid #BCCBC7 !important;
    border-radius: 8px !important;
    caret-color: #087F6E;
}

.stApp input::placeholder,
.stApp textarea::placeholder {
    color: #71818B !important;
    opacity: 1;
}

/* Select boxes */
.stApp [data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #172B4D !important;
    border-color: #BCCBC7 !important;
    border-radius: 8px !important;
}

.stApp [data-baseweb="select"] * {
    color: #172B4D !important;
}

/* Dropdown menu */
[data-baseweb="popover"],
[data-baseweb="menu"],
[data-baseweb="listbox"] {
    background: #FFFFFF !important;
}

[data-baseweb="menu"] *,
[data-baseweb="listbox"] * {
    color: #172B4D !important;
}

[role="option"]:hover {
    background: #E6F4F0 !important;
}

/* Focus state */
.stApp input:focus,
.stApp textarea:focus {
    border-color: #087F6E !important;
    box-shadow: 0 0 0 2px #087F6E22 !important;
}

/* ========================================
   5. BUTTONS
======================================== */
.stButton > button,
.stFormSubmitButton > button,
[data-testid="stDownloadButton"] > button {
    background: var(--primary) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--primary) !important;
    border-radius: 9px !important;
    padding: 0.55rem 1rem;
    font-family: 'DM Sans', sans-serif;
    font-weight: 700;
    transition: all 0.2s ease;
}

.stButton > button *,
.stFormSubmitButton > button *,
[data-testid="stDownloadButton"] > button * {
    color: #FFFFFF !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover,
[data-testid="stDownloadButton"] > button:hover {
    background: var(--primary-dark) !important;
    border-color: var(--primary-dark) !important;
    transform: translateY(-1px);
}

.stButton > button:focus,
.stFormSubmitButton > button:focus {
    box-shadow: 0 0 0 3px #087F6E30 !important;
}

/* ========================================
   6. METRIC CARDS
======================================== */
div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid var(--border);
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(23, 43, 77, 0.05);
}

div[data-testid="stMetric"] label,
div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
    color: #60717D !important;
    font-size: 0.9rem;
    font-weight: 600;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #123B35 !important;
    font-size: 1.8rem;
    font-weight: 700;
}

div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    font-weight: 600;
}

/* ========================================
   7. DATA TABLES
======================================== */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
}

/* ========================================
   8. ALERTS
======================================== */
[data-testid="stAlert"] {
    border-radius: 10px;
    border: 1px solid var(--border);
}

[data-testid="stAlert"] p {
    color: #172B4D !important;
}

/* ========================================
   9. EXPANDERS
======================================== */
[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stExpander"] summary {
    color: #172B4D !important;
    font-weight: 600;
}

[data-testid="stExpander"] summary:hover {
    color: #087F6E !important;
}

/* ========================================
   10. LOGIN HERO SECTION
======================================== */
.hero {
    background: linear-gradient(125deg, #103B35 0%, #087F6E 100%);
    color: #FFFFFF !important;
    padding: 30px;
    border-radius: 18px;
    margin-bottom: 22px;
    box-shadow: 0 8px 24px rgba(16, 59, 53, 0.15);
}

.hero h1,
.hero h2,
.hero h3,
.hero p,
.hero span {
    color: #FFFFFF !important;
}

.hero p {
    color: #D9EAE6 !important;
}

.hero h1 {
    font-size: 2.3rem;
    margin-bottom: 8px;
}

/* ========================================
   11. CHECKBOXES AND RADIO BUTTONS
======================================== */
.stCheckbox label,
.stRadio label {
    color: #263746 !important;
}

.stCheckbox label p,
.stRadio label p {
    color: #263746 !important;
}

/* ========================================
   12. DISABLED CONTROLS
======================================== */
.stApp input:disabled,
.stApp textarea:disabled {
    color: #687782 !important;
    background: #E8EDEF !important;
    opacity: 1;
}

/* ========================================
   13. DIVIDERS AND SPACING
======================================== */
.stApp hr {
    border-color: #DCE5E8;
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
}

/* ========================================
   14. RESPONSIVE LAYOUT
======================================== */
@media (max-width: 768px) {
    [data-testid="stAppViewContainer"] .main .block-container {
        padding: 1rem;
    }

    .stApp h1 {
        font-size: 1.8rem;
    }

    .hero {
        padding: 20px;
        border-radius: 12px;
    }

    .hero h1 {
        font-size: 1.8rem;
    }
}
/* FIX: Sidebar text visibility */
[data-testid="stSidebar"] {
    background-color: #103B35 !important;
}

/* Sidebar text and navigation labels */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] a,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
}

/* Navigation items */
[data-testid="stSidebar"] [role="radiogroup"] label,
[data-testid="stSidebar"] [role="radiogroup"] label p,
[data-testid="stSidebar"] [role="radiogroup"] label span {
    color: #FFFFFF !important;
}

/* Hover effect */
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background-color: #1B5148 !important;
    border-radius: 8px;
}

/* Selected navigation item */
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background-color: #087F6E !important;
    border-radius: 8px;
}

/* Keep sidebar icons visible */
[data-testid="stSidebar"] svg {
    color: #FFFFFF !important;
    fill: currentColor;
}

/* User role and account information */
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #D6E8E4 !important;
}
</style>
""", unsafe_allow_html=True)


# -------------------- DATABASE --------------------

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def pw_hash(password, salt=None):
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt, 180_000
    )
    return salt.hex() + ":" + digest.hex()


def verify_pw(password, stored):
    try:
        salt_hex, digest_hex = stored.split(":", 1)
        test = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            bytes.fromhex(salt_hex),
            180_000,
        ).hex()
        return hmac.compare_digest(test, digest_hex)
    except Exception:
        return False


def init_db():
    with connect() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
                CHECK(role IN ('admin','hr','employee')),
            employee_code TEXT,
            department_id INTEGER,
            designation TEXT DEFAULT 'Staff',
            basic_salary REAL DEFAULT 0,
            join_date TEXT,
            active INTEGER DEFAULT 1,
            must_change_password INTEGER DEFAULT 0,
            FOREIGN KEY(department_id) REFERENCES departments(id)
        );

        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            work_date TEXT NOT NULL,
            check_in TEXT,
            check_out TEXT,
            UNIQUE(user_id, work_date)
        );

        CREATE TABLE IF NOT EXISTS leaves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            leave_type TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            reason TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            reviewer_comment TEXT DEFAULT '',
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            created_by TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS payroll (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            month TEXT NOT NULL,
            basic REAL NOT NULL,
            gross REAL NOT NULL,
            deductions REAL NOT NULL,
            net REAL NOT NULL,
            finalized INTEGER DEFAULT 0,
            UNIQUE(user_id, month)
        );
        """)

        defaults = {
            "company_name": "Demo Company",
            "office_start": "09:00",
            "grace_minutes": "15",
        }

        for key, value in defaults.items():
            conn.execute(
                "INSERT OR IGNORE INTO settings(key,value) VALUES(?,?)",
                (key, value),
            )

        count = conn.execute(
            "SELECT COUNT(*) FROM users"
        ).fetchone()[0]

        if count == 0:
            for dep in [
                "Engineering", "Design", "Sales", "Finance", "Support"
            ]:
                conn.execute(
                    "INSERT INTO departments(name) VALUES(?)", (dep,)
                )

            departments = {
                row["name"]: row["id"]
                for row in conn.execute(
                    "SELECT id,name FROM departments"
                )
            }

            accounts = [
                (
                    "Admin User", "admin@hcm.com", "12345678",
                    "admin", None, None, "Administrator", 0,
                    date.today().isoformat()
                ),
                (
                    "Rabia Tariq (HR)", "hr@hcm.com", "12345678",
                    "hr", None, None, "HR Manager", 0,
                    date.today().isoformat()
                ),
                (
                    "Ayesha Khan", "ayesha@hcm.com", "12345678",
                    "employee", "E001", departments["Engineering"],
                    "Team Lead", 150000,
                    (date.today() - timedelta(days=520)).isoformat()
                ),
                (
                    "Bilal Ahmed", "bilal@hcm.com", "12345678",
                    "employee", "E002", departments["Engineering"],
                    "Developer", 95000,
                    (date.today() - timedelta(days=400)).isoformat()
                ),
                (
                    "Sana Malik", "sana@hcm.com", "12345678",
                    "employee", "E003", departments["Design"],
                    "Designer", 85000,
                    (date.today() - timedelta(days=300)).isoformat()
                ),
                (
                    "Usman Raza", "usman@hcm.com", "12345678",
                    "employee", "E004", departments["Sales"],
                    "Sales Executive", 70000,
                    (date.today() - timedelta(days=260)).isoformat()
                ),
            ]

            for account in accounts:
                name, email, password, role, code, dep, designation, salary, joined = account
                conn.execute("""
                    INSERT INTO users(
                        name,email,password_hash,role,employee_code,
                        department_id,designation,basic_salary,join_date
                    ) VALUES(?,?,?,?,?,?,?,?,?)
                """, (
                    name, email, pw_hash(password), role, code,
                    dep, designation, salary, joined
                ))

            conn.execute("""
                INSERT INTO announcements(
                    title,message,created_by,created_at
                ) VALUES(?,?,?,?)
            """, (
                "Welcome to HCM Lite",
                "This is sample data. Replace it with your company details.",
                "Admin User",
                datetime.now().isoformat(timespec="minutes"),
            ))


init_db()


def query(sql, params=()):
    with connect() as conn:
        return conn.execute(sql, params).fetchall()


def execute(sql, params=()):
    with connect() as conn:
        cursor = conn.execute(sql, params)
        conn.commit()
        return cursor.lastrowid


def setting(key, default=""):
    rows = query("SELECT value FROM settings WHERE key=?", (key,))
    return rows[0]["value"] if rows else default


def employees(active_only=False):
    sql = """
        SELECT u.*, d.name AS department
        FROM users u
        LEFT JOIN departments d ON d.id=u.department_id
        WHERE u.role='employee'
    """
    if active_only:
        sql += " AND u.active=1"
    return query(sql + " ORDER BY u.name")


def money(value):
    return f"Rs {float(value or 0):,.0f}"


def status_today(user_id):
    rows = query(
        "SELECT * FROM attendance WHERE user_id=? AND work_date=?",
        (user_id, date.today().isoformat()),
    )
    if not rows:
        return "Not checked in"
    return "Checked out" if rows[0]["check_out"] else "Checked in"


# -------------------- LOGIN --------------------

def login_screen():
    left, right = st.columns([1.1, 1])

    with left:
        st.markdown("""
        <div class="hero">
            <h1>HCM Lite</h1>
            <h3>People operations, made clearer.</h3>
            <p>Attendance, leave requests and payroll in one place.</p>
            <br>
            <p>3 roles · Attendance tracking · HR dashboard</p>
        </div>
        """, unsafe_allow_html=True)

        st.info(
            "This demo uses sample accounts. Change demo passwords "
            "before using real data."
        )

    with right:
        st.subheader("Welcome back")

        with st.form("login_form"):
            email = st.text_input(
                "Email", placeholder="admin@hcm.com"
            ).strip().lower()
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button(
                "Sign in", use_container_width=True
            )

        if submitted:
            rows = query(
                "SELECT * FROM users WHERE lower(email)=? AND active=1",
                (email,),
            )
            if rows and verify_pw(password, rows[0]["password_hash"]):
                st.session_state.user = dict(rows[0])
                st.rerun()
            else:
                st.error("Email or password is incorrect.")

        with st.expander("Demo login accounts"):
            st.code(
                "Admin:    admin@hcm.com / 12345678\n"
                "HR:       hr@hcm.com / 12345678\n"
                "Employee: ayesha@hcm.com / 12345678"
            )


# -------------------- ANNOUNCEMENTS --------------------

def show_announcements():
    rows = query(
        "SELECT * FROM announcements ORDER BY id DESC LIMIT 10"
    )

    if not rows:
        st.caption("No announcements yet.")

    for row in rows:
        with st.container(border=True):
            st.markdown(f'**{row["title"]}**')
            st.write(row["message"])
            st.caption(f'{row["created_by"]} · {row["created_at"]}')


# -------------------- DASHBOARD --------------------

def page_dashboard(user):
    today = date.today().isoformat()

    st.markdown(
        f'<div class="hero"><h1>Good day, '
        f'{user["name"].split()[0]} 👋</h1>'
        f'<p>{setting("company_name", "HCM Lite")} · '
        f'{date.today().strftime("%A, %d %B %Y")}</p></div>',
        unsafe_allow_html=True,
    )

    if user["role"] == "employee":
        attendance = query(
            "SELECT * FROM attendance WHERE user_id=? AND work_date=?",
            (user["id"], today),
        )
        leave_count = query(
            "SELECT COUNT(*) n FROM leaves "
            "WHERE user_id=? AND status='Pending'",
            (user["id"],),
        )[0]["n"]
        pays = query(
            "SELECT * FROM payroll WHERE user_id=? "
            "ORDER BY month DESC LIMIT 1",
            (user["id"],),
        )

        a, b, c = st.columns(3)
        a.metric("Today", status_today(user["id"]))
        b.metric("Pending leave requests", leave_count)
        c.metric(
            "Last payslip",
            money(pays[0]["net"]) if pays else "Not available",
        )

        st.subheader("Attendance")

        if not attendance:
            if st.button("Check in", type="primary"):
                execute(
                    "INSERT INTO attendance(user_id,work_date,check_in) "
                    "VALUES(?,?,?)",
                    (user["id"], today, datetime.now().strftime("%H:%M")),
                )
                st.rerun()
        elif not attendance[0]["check_out"]:
            st.success(f'Checked in at {attendance[0]["check_in"]}')
            if st.button("Check out"):
                execute(
                    "UPDATE attendance SET check_out=? "
                    "WHERE user_id=? AND work_date=?",
                    (
                        datetime.now().strftime("%H:%M"),
                        user["id"], today,
                    ),
                )
                st.rerun()
        else:
            st.success(
                f'Checked in at {attendance[0]["check_in"]} and '
                f'checked out at {attendance[0]["check_out"]}.'
            )

        st.subheader("Announcements")
        show_announcements()
        return

    active = employees(True)
    attendance_rows = query("""
        SELECT a.*,u.name FROM attendance a
        JOIN users u ON u.id=a.user_id
        WHERE a.work_date=?
    """, (today,))
    pending = query(
        "SELECT COUNT(*) n FROM leaves WHERE status='Pending'"
    )[0]["n"]

    payroll_total = sum(
        float(employee["basic_salary"] or 0) * 1.5
        for employee in active
    )

    a, b, c, d = st.columns(4)
    a.metric("Active employees", len(active))
    b.metric("Checked in today", len(attendance_rows))
    c.metric("Pending leave requests", pending)
    d.metric("Estimated gross payroll", money(payroll_total))

    st.subheader("Today's attendance")
    if attendance_rows:
        st.dataframe(
            pd.DataFrame([dict(row) for row in attendance_rows])[
                ["name", "work_date", "check_in", "check_out"]
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No attendance check-ins recorded today yet.")

    if active:
        df = pd.DataFrame([dict(row) for row in active])
        st.subheader("Employees by department")
        counts = (
            df["department"].fillna("Unassigned")
            .value_counts()
            .rename_axis("Department")
            .reset_index(name="Employees")
        )
        st.bar_chart(counts.set_index("Department"))

    st.subheader("Announcements")
    show_announcements()


# -------------------- EMPLOYEES --------------------

def page_employees(user):
    st.title("Employees")

    if user["role"] in ("admin", "hr"):
        with st.expander("➕ Register employee"):
            # IMPORTANT FIX:
            # Convert sqlite3.Row objects to normal dictionaries.
            departments = [
                dict(row)
                for row in query(
                    "SELECT * FROM departments ORDER BY name"
                )
            ]

            if not departments:
                st.warning("Create a department first.")

            with st.form("add_employee"):
                name = st.text_input("Full name")
                email = st.text_input("Email").strip().lower()
                code = st.text_input(
                    "Employee code",
                    value=f'E{len(employees()) + 1:03d}',
                )

                department = (
                    st.selectbox(
                        "Department",
                        options=departments,
                        format_func=lambda item: item["name"],
                    )
                    if departments else None
                )

                designation = st.text_input(
                    "Designation", value="Staff"
                )
                salary = st.number_input(
                    "Basic monthly salary (PKR)",
                    min_value=0.0,
                    value=50000.0,
                    step=5000.0,
                )
                joined = st.date_input(
                    "Joining date", value=date.today()
                )
                temporary_password = st.text_input(
                    "Initial password (minimum 8 characters)",
                    type="password",
                )
                submitted = st.form_submit_button("Register employee")

            if submitted:
                if (
                    not name.strip()
                    or "@" not in email
                    or len(temporary_password) < 8
                    or not department
                ):
                    st.error(
                        "Enter a name, valid email, department, "
                        "and password of at least 8 characters."
                    )
                else:
                    try:
                        execute("""
                            INSERT INTO users(
                                name,email,password_hash,role,
                                employee_code,department_id,designation,
                                basic_salary,join_date,must_change_password
                            )
                            VALUES(?,?,?,'employee',?,?,?,?,?,1)
                        """, (
                            name.strip(),
                            email,
                            pw_hash(temporary_password),
                            code.strip(),
                            department["id"],
                            designation.strip() or "Staff",
                            salary,
                            joined.isoformat(),
                        ))
                        st.success("Employee registered successfully.")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error(
                            "That email or employee code may already "
                            "be in use."
                        )

    rows = employees()

    if rows:
        df = pd.DataFrame([dict(row) for row in rows])
        search = st.text_input(
            "Search by name, email, code or department"
        )

        if search:
            mask = (
                df[["name", "email", "employee_code", "department"]]
                .fillna("")
                .astype(str)
                .apply(
                    lambda col: col.str.contains(
                        search, case=False, regex=False
                    )
                )
                .any(axis=1)
            )
            df = df[mask]

        columns = [
            "employee_code", "name", "email", "department",
            "designation", "basic_salary", "join_date", "active",
        ]

        st.dataframe(
            df[columns].rename(columns={
                "employee_code": "Code",
                "name": "Name",
                "email": "Email",
                "department": "Department",
                "designation": "Designation",
                "basic_salary": "Basic salary (PKR)",
                "join_date": "Joined",
                "active": "Active",
            }),
            use_container_width=True,
            hide_index=True,
        )

        if user["role"] == "admin":
            with st.expander("Deactivate / reactivate employee"):
                employee_options = [dict(row) for row in rows]

                employee = st.selectbox(
                    "Select employee",
                    options=employee_options,
                    format_func=lambda item: (
                        f'{item["name"]} '
                        f'({"active" if item["active"] else "inactive"})'
                    ),
                )

                if st.button("Toggle active status"):
                    execute(
                        "UPDATE users SET active=? WHERE id=?",
                        (
                            0 if employee["active"] else 1,
                            employee["id"],
                        ),
                    )
                    st.success("Employee status updated.")
                    st.rerun()
    else:
        st.info("No employees registered yet.")


# -------------------- ATTENDANCE --------------------

def page_attendance(user):
    st.title("Attendance")

    if user["role"] == "employee":
        rows = query("""
            SELECT work_date,check_in,check_out
            FROM attendance
            WHERE user_id=?
            ORDER BY work_date DESC LIMIT 60
        """, (user["id"],))
    else:
        rows = query("""
            SELECT a.work_date,u.name,u.employee_code,
                   a.check_in,a.check_out
            FROM attendance a
            JOIN users u ON u.id=a.user_id
            ORDER BY a.work_date DESC,a.check_in DESC
            LIMIT 500
        """)

        col1, col2 = st.columns(2)
        start = col1.date_input(
            "From date",
            value=date.today() - timedelta(days=30),
            key="att_from",
        )
        end = col2.date_input(
            "To date", value=date.today(), key="att_to"
        )

        rows = [
            row for row in rows
            if start.isoformat() <= row["work_date"] <= end.isoformat()
        ]

    if rows:
        df = pd.DataFrame([dict(row) for row in rows])
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "Download attendance CSV",
            df.to_csv(index=False).encode("utf-8"),
            "attendance.csv",
            "text/csv",
        )
    else:
        st.info("No attendance records found for this period.")


# -------------------- LEAVE MANAGEMENT --------------------

def page_leave(user):
    st.title("Leave management")

    if user["role"] == "employee":
        with st.expander("📝 Apply for leave"):
            with st.form("leave_form"):
                leave_type = st.selectbox(
                    "Leave type", ["Annual", "Sick", "Casual", "Unpaid"]
                )
                col1, col2 = st.columns(2)
                start = col1.date_input(
                    "First day", value=date.today() + timedelta(days=1)
                )
                end = col2.date_input(
                    "Last day", value=date.today() + timedelta(days=1)
                )
                reason = st.text_area(
                    "Reason (at least 10 characters)"
                )
                submitted = st.form_submit_button("Submit request")

            if submitted:
                if end < start or len(reason.strip()) < 10:
                    st.error(
                        "Check the date range and enter a reason "
                        "of at least 10 characters."
                    )
                else:
                    execute("""
                        INSERT INTO leaves(
                            user_id,leave_type,start_date,end_date,
                            reason,status,created_at
                        ) VALUES(?,?,?,?,?,?,?)
                    """, (
                        user["id"], leave_type,
                        start.isoformat(), end.isoformat(),
                        reason.strip(), "Pending",
                        datetime.now().isoformat(timespec="minutes"),
                    ))
                    st.success("Leave request submitted.")
                    st.rerun()

        rows = query(
            "SELECT * FROM leaves WHERE user_id=? ORDER BY id DESC",
            (user["id"],),
        )
    else:
        status_filter = st.selectbox(
            "Show requests", ["Pending", "All", "Approved", "Rejected"]
        )

        sql = """
            SELECT l.*,u.name,u.employee_code
            FROM leaves l JOIN users u ON u.id=l.user_id
        """
        params = ()

        if status_filter != "All":
            sql += " WHERE l.status=?"
            params = (status_filter,)

        rows = query(sql + " ORDER BY l.id DESC", params)

    if rows:
        for row in rows:
            title = (
                f'{row["leave_type"]} · {row["start_date"]} to '
                f'{row["end_date"]} · {row["status"]}'
            )

            with st.expander(title):
                if user["role"] != "employee":
                    st.write(
                        f'**Employee:** {row["name"]} '
                        f'({row["employee_code"] or "—"})'
                    )

                st.write(f'**Reason:** {row["reason"]}')

                if row["reviewer_comment"]:
                    st.write(
                        f'**Reviewer comment:** {row["reviewer_comment"]}'
                    )

                if (
                    user["role"] in ("admin", "hr")
                    and row["status"] == "Pending"
                ):
                    comment = st.text_input(
                        "Reviewer comment (optional)",
                        key=f'comment_{row["id"]}',
                    )

                    col1, col2 = st.columns(2)

                    if col1.button(
                        "Approve",
                        key=f'approve_{row["id"]}',
                        type="primary",
                    ):
                        execute(
                            "UPDATE leaves SET status=?,reviewer_comment=? "
                            "WHERE id=?",
                            ("Approved", comment, row["id"]),
                        )
                        st.success("Leave approved.")
                        st.rerun()

                    if col2.button(
                        "Reject", key=f'reject_{row["id"]}'
                    ):
                        execute(
                            "UPDATE leaves SET status=?,reviewer_comment=? "
                            "WHERE id=?",
                            ("Rejected", comment, row["id"]),
                        )
                        st.warning("Leave rejected.")
                        st.rerun()
    else:
        st.info("No leave requests to show.")


# -------------------- PAYROLL --------------------

def page_payroll(user):
    st.title("Payroll")

    if user["role"] in ("admin", "hr"):
        with st.expander("⚙️ Generate monthly payroll"):
            month = st.text_input(
                "Payroll month (YYYY-MM)",
                value=date.today().strftime("%Y-%m"),
            )

            st.caption(
                "Demo calculation: gross salary = 1.5 × basic salary. "
                "Tax and attendance deductions are not included."
            )

            if st.button("Generate / refresh payroll", type="primary"):
                try:
                    datetime.strptime(month, "%Y-%m")

                    for employee in employees(True):
                        basic = float(employee["basic_salary"] or 0)
                        gross = basic * 1.5

                        execute("""
                            INSERT INTO payroll(
                                user_id,month,basic,gross,deductions,net,finalized
                            ) VALUES(?,?,?,?,?,?,0)
                            ON CONFLICT(user_id,month) DO UPDATE SET
                                basic=excluded.basic,
                                gross=excluded.gross,
                                deductions=excluded.deductions,
                                net=excluded.net
                            WHERE payroll.finalized=0
                        """, (
                            employee["id"], month,
                            basic, gross, 0.0, gross,
                        ))

                    st.success(f"Payroll generated for {month}.")
                    st.rerun()

                except ValueError:
                    st.error(
                        "Enter the month as YYYY-MM, for example 2026-10."
                    )

        rows = query("""
            SELECT p.*,u.name,u.employee_code
            FROM payroll p JOIN users u ON u.id=p.user_id
            ORDER BY p.month DESC,u.name
        """)
    else:
        rows = query("""
            SELECT p.*,u.name,u.employee_code
            FROM payroll p JOIN users u ON u.id=p.user_id
            WHERE p.user_id=? AND p.finalized=1
            ORDER BY p.month DESC
        """, (user["id"],))

    if rows:
        df = pd.DataFrame([dict(row) for row in rows])

        st.dataframe(
            df[[
                "month", "employee_code", "name", "basic",
                "gross", "deductions", "net", "finalized",
            ]].rename(columns={
                "month": "Month",
                "employee_code": "Code",
                "name": "Employee",
                "basic": "Basic (PKR)",
                "gross": "Gross (PKR)",
                "deductions": "Deductions (PKR)",
                "net": "Net pay (PKR)",
                "finalized": "Finalized",
            }),
            use_container_width=True,
            hide_index=True,
        )

        if user["role"] == "admin":
            months = sorted(
                {row["month"] for row in rows if not row["finalized"]},
                reverse=True,
            )

            if months:
                month_choice = st.selectbox(
                    "Finalize payroll month", months
                )

                if st.button("Finalize selected month"):
                    execute(
                        "UPDATE payroll SET finalized=1 WHERE month=?",
                        (month_choice,),
                    )
                    st.success(
                        "Payroll finalized. Employee payslips are now visible."
                    )
                    st.rerun()
    else:
        st.info("No payroll records available yet.")


# -------------------- COMPANY SETTINGS --------------------

def page_company(user):
    st.title("Company setup")

    if user["role"] != "admin":
        st.info(f'Company: {setting("company_name", "HCM Lite")}')
        return

    with st.form("company_settings"):
        company = st.text_input(
            "Company name", value=setting("company_name", "Demo Company")
        )
        office_start = st.time_input(
            "Office start time",
            value=datetime.strptime(
                setting("office_start", "09:00"), "%H:%M"
            ).time(),
        )
        grace = st.number_input(
            "Grace period (minutes)",
            min_value=0,
            max_value=180,
            value=int(setting("grace_minutes", "15")),
        )
        save = st.form_submit_button("Save company settings")

    if save:
        settings = [
            ("company_name", company.strip()),
            ("office_start", office_start.strftime("%H:%M")),
            ("grace_minutes", str(grace)),
        ]

        for key, value in settings:
            execute("""
                INSERT INTO settings(key,value) VALUES(?,?)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value
            """, (key, value))

        st.success("Settings saved.")
        st.rerun()

    st.subheader("Departments")

    with st.form("department_form"):
        department_name = st.text_input("New department name")
        add = st.form_submit_button("Add department")

    if add:
        if not department_name.strip():
            st.error("Enter a department name.")
        else:
            try:
                execute(
                    "INSERT INTO departments(name) VALUES(?)",
                    (department_name.strip(),),
                )
                st.success("Department added.")
                st.rerun()
            except sqlite3.IntegrityError:
                st.error("That department already exists.")

    departments = query("SELECT * FROM departments ORDER BY name")

    if departments:
        st.dataframe(
            pd.DataFrame([dict(row) for row in departments]),
            use_container_width=True,
            hide_index=True,
        )


# -------------------- ANNOUNCEMENT MANAGEMENT --------------------

def page_announcements(user):
    st.title("Announcements")

    if user["role"] in ("admin", "hr"):
        with st.form("announcement_form"):
            title = st.text_input("Title")
            message = st.text_area("Message")
            submitted = st.form_submit_button("Publish announcement")

        if submitted:
            if title.strip() and message.strip():
                execute("""
                    INSERT INTO announcements(
                        title,message,created_by,created_at
                    ) VALUES(?,?,?,?)
                """, (
                    title.strip(),
                    message.strip(),
                    user["name"],
                    datetime.now().isoformat(timespec="minutes"),
                ))
                st.success("Announcement published.")
                st.rerun()
            else:
                st.error("Enter both a title and message.")

    show_announcements()


# -------------------- PROFILE --------------------

def page_profile(user):
    st.title("My profile")

    st.write(f'**Name:** {user["name"]}')
    st.write(f'**Email:** {user["email"]}')
    st.write(f'**Role:** {user["role"].title()}')

    with st.form("change_password"):
        old = st.text_input("Current password", type="password")
        new = st.text_input(
            "New password (at least 8 characters)", type="password"
        )
        confirm = st.text_input("Confirm new password", type="password")
        submitted = st.form_submit_button("Change password")

    if submitted:
        rows = query(
            "SELECT password_hash FROM users WHERE id=?",
            (user["id"],),
        )
        current = rows[0]["password_hash"]

        if not verify_pw(old, current):
            st.error("Current password is incorrect.")
        elif len(new) < 8:
            st.error("New password must be at least 8 characters.")
        elif new != confirm:
            st.error("Passwords do not match.")
        else:
            execute(
                "UPDATE users SET password_hash=?,must_change_password=0 "
                "WHERE id=?",
                (pw_hash(new), user["id"]),
            )
            st.success("Password changed successfully.")


# -------------------- MAIN APP --------------------

def main():
    if "user" not in st.session_state:
        st.session_state.user = None

    if not st.session_state.user:
        login_screen()
        return

    user = st.session_state.user

    fresh = query("""
        SELECT u.*,d.name AS department
        FROM users u
        LEFT JOIN departments d ON d.id=u.department_id
        WHERE u.id=?
    """, (user["id"],))

    if not fresh or not fresh[0]["active"]:
        st.session_state.user = None
        st.rerun()
        return

    user = dict(fresh[0])
    st.session_state.user = user

    with st.sidebar:
        st.markdown("## HCM Lite")
        st.caption(f'{user["name"]} · {user["role"].title()}')

        options = [
            "Dashboard",
            "Employees",
            "Attendance",
            "Leave management",
            "Payroll",
            "Announcements",
            "My profile",
        ]

        if user["role"] == "admin":
            options.append("Company setup")

        page = st.radio(
            "Navigation",
            options,
            label_visibility="collapsed",
        )

        st.divider()

        if st.button("Sign out", use_container_width=True):
            st.session_state.user = None
            st.rerun()

        st.caption("HCM Lite · Streamlit edition")

    if page == "Dashboard":
        page_dashboard(user)
    elif page == "Employees":
        page_employees(user)
    elif page == "Attendance":
        page_attendance(user)
    elif page == "Leave management":
        page_leave(user)
    elif page == "Payroll":
        page_payroll(user)
    elif page == "Announcements":
        page_announcements(user)
    elif page == "My profile":
        page_profile(user)
    elif page == "Company setup":
        page_company(user)


main()