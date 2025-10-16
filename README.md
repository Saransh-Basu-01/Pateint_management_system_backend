# 🏥 Patient Management System API (FastAPI CRUD Project)

## 📘 Overview
This is my **first FastAPI backend project** — a **Patient Management System API** that allows you to **create, view, edit, sort, and delete** patient records.  
It’s a simple yet complete **CRUD (Create, Read, Update, Delete)** backend built using **FastAPI** and **Pydantic**, with data stored in a local JSON file.

---

## 🚀 Features
✅ Create new patient records  
✅ View all patients or a specific patient by ID  
✅ Edit or update existing patient details  
✅ Delete patient records  
✅ Sort patients by `height`, `weight`, or computed `BMI`  
✅ Automatically compute **BMI** and give a **health verdict**  
✅ Full validation using **Pydantic models**

---

## 🧠 Tech Stack
- **Backend Framework:** FastAPI  
- **Validation:** Pydantic  
- **Storage:** JSON file  
- **Response Handling:** FastAPI’s `JSONResponse`  
- **Language:** Python 3.10+  

---

## ⚙️ Installation & Setup

### 1️⃣ Clone this repository
```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
pip install fastapi uvicorn
uvicorn main:app --reload
```
