# ---- frontend build stage ----
FROM node:20-slim AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# ---- backend runtime stage ----
FROM python:3.11-slim

# libreoffice-writer: headless docx->pdf conversion (Vakifbank transfer + Invoice docs)
# fontconfig: needed to register the bundled CJK font below
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice-writer \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# Register the bundled Noto Sans SC with the system so LibreOffice can find
# it by name — Debian's own fontconfig works correctly (unlike the macOS
# LibreOffice cask used in local dev), this just avoids depending on
# whichever CJK font package name a given base image happens to ship.
RUN cp app/assets/fonts/NotoSansSC.ttf /usr/local/share/fonts/NotoSansSC.ttf && fc-cache -f

COPY --from=frontend-build /app/frontend/dist ./static

RUN mkdir -p /app/data

ENV PORT=8000
EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
