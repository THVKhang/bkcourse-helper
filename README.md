# 🎓 BKCourse Helper

> Công cụ hỗ trợ chọn môn & xếp lịch thông minh dành cho sinh viên **HCMUT (Đại học Bách Khoa TP.HCM)**.

![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-blue)

---

## ✨ Tính năng chính

### 📅 Xếp lịch thông minh (`/planner`)
Quy trình 4 bước đơn giản:
1. **Paste dữ liệu** — Copy bảng đăng ký từ MyBK portal, dán vào hệ thống
2. **Chọn môn học** — Chọn các môn muốn xếp lịch
3. **Tạo lịch** — Hệ thống tự động tạo nhiều phương án (gom ngày, sáng/chiều, cân bằng...)
4. **Xuất kết quả** — Tải về dạng **Excel** hoặc file **.ics** (Google Calendar / Apple Calendar)

### 📚 Chương trình học (`/study-plan`)
- Hiển thị chương trình đào tạo **Khoa học Máy tính — Khóa 2024** (128 tín chỉ)
- Liệt kê môn học theo từng học kỳ (HK 1–8), phân loại **Bắt buộc / Tự chọn**
- ✅ Tích xanh môn đã đậu → tự động đếm tín chỉ tích lũy
- ⚡ Nút **"Tích hết"** để đánh dấu nhanh cả học kỳ
- 🔮 **Gợi ý môn tiếp theo** — tự động đề xuất các môn bắt buộc chưa hoàn thành
- 📊 Progress ring + thống kê nhanh theo từng HK
- Dữ liệu lưu trong `localStorage` (không cần đăng nhập)

---

## 🏗️ Kiến trúc

```
bkcourse-helperTHVK/
├── frontend/          # Next.js 14 (React, TailwindCSS)
│   ├── src/app/       # Pages: /, /planner, /study-plan
│   ├── src/lib/       # API client, types, export utils
│   └── src/components/# UI components (Navbar, ThemeProvider...)
├── backend/           # FastAPI (Python)
│   ├── app/api/       # REST routes
│   ├── app/models/    # SQLAlchemy models
│   ├── app/services/  # Business logic
│   └── app/parsers/   # HCMUT portal data parser
├── scripts/           # Seed & crawl scripts (seed_cs2024.py, seed_prerequisites.py...)
├── sql/               # SQL schema & queries tham khảo
├── package.json       # Root config (Vercel experimentalServices)
└── vercel.json        # Vercel deployment config
```

---

## 🚀 Cài đặt & Chạy local

### Yêu cầu
- **Node.js** ≥ 18
- **Python** ≥ 3.10

### 1. Clone repo
```bash
git clone https://github.com/THVKhang/bkcourse-helperTHVK.git
cd bkcourse-helperTHVK
```

### 2. Cài đặt Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

### 3. Cấu hình Backend
Tạo file `backend/.env`:
```env
# Chọn 1 trong 2:
DB_URL=sqlite:///./bkcourse.db                          # SQLite (local)
# DB_URL=postgresql://user:pass@host:5432/dbname        # PostgreSQL (production)

CORS_ORIGINS=http://localhost:3000
DEBUG=1

# Bắt buộc khi deploy production (>= 32 ký tự)
JWT_SECRET=<chuỗi-bí-mật-ngẫu-nhiên>
# Tuỳ chọn: gửi email đặt lại mật khẩu qua Resend
RESEND_API_KEY=
```

> Có thể copy nhanh từ `backend/.env.example`. Nếu không có `.env`, backend mặc định dùng SQLite `bkcourse.db`.

### 4. Khởi tạo Database & Seed dữ liệu
```bash
# Từ thư mục backend/
python -c "from app.main import app"      # Tạo tables
python ../scripts/seed_cs2024.py          # Seed chương trình CS 2024
python ../scripts/seed_prerequisites.py   # Seed môn tiên quyết
```

### 5. Cài đặt Frontend
```bash
cd ../frontend
npm install
```

### 6. Chạy ứng dụng
Mở **2 terminal** riêng biệt:

```bash
# Terminal 1 — Backend (port 8000)
cd backend
venv\Scripts\python.exe -m uvicorn app.main:app --port 8000 --reload

# Terminal 2 — Frontend (port 3000)
cd frontend
npm run dev
```

Truy cập: **http://localhost:3000**

Hoặc chạy cả 2 bằng một lệnh: `npm run dev` (Windows, dùng `dev.ps1`) hoặc `./dev.sh` (macOS/Linux).

### 7. Chạy test
```bash
cd backend
pip install -r requirements-dev.txt
python -m pytest -q
```

```bash
cd frontend
npx tsc --noEmit && npm run build
```

CI (GitHub Actions — `.github/workflows/ci.yml`) tự động chạy test backend và build frontend cho mỗi push/PR.

---

## ☁️ Deploy lên Vercel

Project đã được cấu hình sẵn cho Vercel monorepo deployment:

1. Push code lên GitHub
2. Import repo trên [vercel.com](https://vercel.com)
3. Thêm Environment Variable: `DB_URL` = `sqlite:///./bkcourse.db`
   và `JWT_SECRET` = chuỗi bí mật ngẫu nhiên (dùng để ký token đăng nhập)
4. Deploy!

> **Lưu ý:** SQLite trên Vercel chạy ở chế độ read-only (serverless). Trang **Chương trình học** vẫn hoạt động bình thường vì lưu state ở `localStorage`. Để lưu dữ liệu phía server trên production, cần chuyển sang database cloud (Supabase/Neon PostgreSQL).

---

## 🛠️ Tech Stack

| Layer | Công nghệ |
|-------|-----------|
| Frontend | Next.js 14, React 18, TailwindCSS, Radix UI, Lucide Icons |
| Backend | FastAPI, SQLAlchemy 2.0, Pydantic v2 |
| Database | SQLite (local) |
| Export | xlsx (Excel), iCal (.ics) |
| Deploy | Vercel (experimentalServices) |

---

## 📝 API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| `GET` | `/programs` | Danh sách chương trình đào tạo |
| `GET` | `/programs/{id}/plan` | Kế hoạch giảng dạy theo HK |
| `POST` | `/imports/paste` | Parse dữ liệu từ MyBK portal |
| `POST` | `/schedule/generate` | Tạo các phương án xếp lịch |
| `GET` | `/students/{code}/history` | Lịch sử học tập sinh viên |
| `POST` | `/recommendations` | Gợi ý môn học HK tới |
| `POST` | `/auth/register`, `/auth/login`, `/auth/guest` | Đăng ký / đăng nhập / khách |
| `GET` | `/auth/me` | Thông tin người dùng hiện tại |
| `POST` | `/share` · `GET` `/share/{id}` | Chia sẻ thời khoá biểu |
| `GET` | `/health` | Health check |

---

## 👨‍💻 Tác giả

**THVKhang** — Sinh viên HCMUT

---

## 📄 License

MIT License — Tự do sử dụng và chỉnh sửa.
