from flask import Flask, render_template_string, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# تهيئة قاعدة البيانات عند أول تشغيل
@app.before_first_request
def before_first_request():
    init_db()

# صفحة تسجيل الدخول
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # التحقق من اسم المستخدم وكلمة المرور
        conn = sqlite3.connect('rezdar_financial.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return redirect(url_for("dashboard"))
        else:
            flash("اسم المستخدم أو كلمة المرور غير صحيحة", "error")
    return render_template_string(HTML_TEMPLATE)

# صفحة اللوحة الرئيسية بعد تسجيل الدخول
@app.route("/dashboard")
def dashboard():
    return render_template_string(DASHBOARD_TEMPLATE)

# صفحة الإرسال
@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        sender_name = request.form["sender_name"]
        recipient_name = request.form["recipient_name"]
        sender_phone = request.form["sender_phone"]
        recipient_phone = request.form["recipient_phone"]
        destination = request.form["destination"]
        amount = request.form["amount"]
        currency = request.form["currency"]
        commission_status = request.form["commission_status"]

        # حفظ المعاملة في قاعدة البيانات
        conn = sqlite3.connect('rezdar_financial.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO transactions (sender_name, recipient_name, sender_phone, recipient_phone, destination, amount, currency, commission_status) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (sender_name, recipient_name, sender_phone, recipient_phone, destination, amount, currency, commission_status))
        conn.commit()
        conn.close()
        flash("تم إرسال المعاملة بنجاح", "success")
        return redirect(url_for("send"))

    return render_template_string(SEND_TEMPLATE)

# صفحة الاستلام
@app.route("/receive", methods=["GET", "POST"])
def receive():
    if request.method == "POST":
        notification_id = request.form["notification_id"]

        conn = sqlite3.connect('rezdar_financial.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE id = ?", (notification_id,))
        transaction = cursor.fetchone()
        conn.close()

        if transaction:
            return render_template_string(RECEIVE_TEMPLATE, transaction=transaction)
        else:
            flash("لم يتم العثور على المعاملة", "error")
            return redirect(url_for("receive"))

    return render_template_string(RECEIVE_FORM_TEMPLATE)

# تهيئة قاعدة البيانات
def init_db():
    conn = sqlite3.connect('rezdar_financial.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sender_name TEXT,
                        recipient_name TEXT,
                        sender_phone TEXT,
                        recipient_phone TEXT,
                        destination TEXT,
                        amount REAL,
                        currency TEXT,
                        commission_status TEXT,
                        is_received INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

# HTML Templates داخل Python
HTML_TEMPLATE = '''...'''  # ضع كود HTML الخاص بتسجيل الدخول هنا.
DASHBOARD_TEMPLATE = '''...'''  # ضع كود HTML الخاص باللوحة الرئيسية هنا.
SEND_TEMPLATE = '''...'''  # ضع كود HTML الخاص بصفحة الإرسال هنا.
RECEIVE_FORM_TEMPLATE = '''...'''  # ضع كود HTML الخاص بنموذج الاستلام هنا.
RECEIVE_TEMPLATE = '''...'''  # ضع كود HTML الخاص بعرض المعاملة عند الاستلام هنا.

if __name__ == "__main__":
    app.run(debug=True)
