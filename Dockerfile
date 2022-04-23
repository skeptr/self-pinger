FROM python:3.9-alpine as build_deps
WORKDIR /build/
COPY requirements.txt .
RUN python -m venv ./venv
RUN ./venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.9-alpine as production
WORKDIR /opt/app
EXPOSE 8000
COPY application/ .
COPY --from=build_deps /build/venv ./venv
USER nobody
CMD [ "./venv/bin/python", "main.py" ]
HEALTHCHECK\
  --interval=30s\
  --timeout=3s\
  --retries=3\
  --start-period=5s\ 
  CMD wget --spider http://localhost:8000
