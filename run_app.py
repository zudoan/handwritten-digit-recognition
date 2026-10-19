"""
Main launcher script for the Handwritten Digit Recognition Web Application.
Nhóm 03 - Môn Nhận dạng mẫu
Runs the FastAPI web server on http://127.0.0.1:8000
"""
import sys
import uvicorn
from pathlib import Path

# UTF-8 stdout configuration for Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

if __name__ == "__main__":
    print("=" * 65)
    print("KHỞI ĐỘNG HỆ THỐNG DEMO NHẬN DẠNG CHỮ SỐ VIẾT TAY (MNIST)")
    print("BÀI TẬP LỚN MÔN NHẬN DẠNG MẪU - NHÓM 03")
    print("Truy cập ứng dụng tại: http://127.0.0.1:8000")
    print("=" * 65)

    uvicorn.run("app.server:app", host="127.0.0.1", port=8000, reload=False)
