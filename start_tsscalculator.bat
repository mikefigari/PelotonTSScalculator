@echo off
cd /d "%~dp0"
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
