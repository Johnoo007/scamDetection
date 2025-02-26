from flask import Flask, request, render_template, session, redirect, url_for
import pickle

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # ใช้สำหรับเก็บ session

# 🔹 โหลดโมเดลที่บันทึกไว้
with open("scam_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# 📌 ฟังก์ชันทำนาย  
def predict_scam(text):
    prediction = model.predict([text])[0]
    if prediction == 1:
        return "ความเสี่ยงสูงที่จะเป็นการหลอกลวง 🚨"
    elif prediction == 0:
        return "Not Scam ✅"
    else:
        return "ความเสี่ยงปานกลาง 🤔"

# 🌍 Route หน้าเว็บหลัก
@app.route("/", methods=["GET", "POST"])
def index():
    if 'history' not in session:
        session['history'] = []

    if request.method == "POST":
        user_input = request.form["message"]
        result = predict_scam(user_input)

        # เพิ่มข้อความและผลลัพธ์ลงใน history
        session['history'].append({"message": user_input, "result": result})
        session.modified = True  # บอก Flask ว่า session มีการเปลี่ยนแปลง

    return render_template("index.html", history=session['history'])

@app.route("/clear", methods=["POST"])
def clear_history():
    session.pop('history', None)  # ลบ history ออกจาก session
    session.modified = True
    return redirect(url_for("index"))  # redirect กลับไปหน้า index

# 🚀 รัน Flask Server
if __name__ == "__main__":
    app.run(debug=True)
