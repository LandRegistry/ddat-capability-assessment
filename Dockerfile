FROM python:3.11-slim

RUN useradd containeruser

WORKDIR /home/containeruser

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

COPY app app
COPY ddat-capability-assessment.py config.py docker-entrypoint.sh requirements.txt ./
RUN pip install -r requirements.txt \
    && chmod +x docker-entrypoint.sh \
    && chown -R containeruser:containeruser ./

# Set environment variables
ENV CONTACT_EMAIL="[contact email]" \
    CONTACT_PHONE="[contact phone]" \
    DATABASE_URL="postgresql://mash:mash@localhost:5432/capability" \
    DEPARTMENT_NAME="HM Land Registry" \
    DEPARTMENT_URL="https://www.gov.uk/government/organisations/land-registry" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    REDIS_URL="redis://redis:6379" \
    SECRET_KEY=4f378500459bb58fecf903ea3c113069f11f150b33388f56fc89f7edce0e6a84 \
    SERVICE_NAME="DDaT Capability Assessment" \
    SERVICE_PHASE="Alpha" \
    SERVICE_URL="[url of service]"

USER containeruser

EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]