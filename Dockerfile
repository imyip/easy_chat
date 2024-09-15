FROM python:3.11-slim AS build-venv
RUN python3 -m venv /venv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 

FROM gcr.io/distroless/python3
COPY --from=build-venv /venv /venv
EXPOSE 8501
COPY streamlit_app.py streamlit_app.py
ENTRYPOINT ["/venv/bin/python3 && streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0"]


