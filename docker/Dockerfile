FROM python:3.12.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MPLCONFIGDIR=/tmp/matplotlib \
    IPYTHONDIR=/tmp/ipython \
    OPENBLAS_NUM_THREADS=2 \
    OMP_NUM_THREADS=2

WORKDIR /workspace
COPY docker/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

EXPOSE 8888
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]

# docker compose -f ./docker/compose.yaml up -d && docker compose -f ./docker/compose.yaml attach demo
# jupyter lab --allow-root --no-browser --ip=0.0.0.0 --notebook-dir=/workspace
