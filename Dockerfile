FROM hub.misaka.games/library/python:3.11-slim AS base

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM gcr.io/distroless/python3

COPY --from=base /usr/local/lib/python3.11/site-packages/ /usr/lib/python3.11/dist-packages/
COPY streamlit_app.py streamlit_app.py

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
