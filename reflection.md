# Reflection — Dockerizing QR Code Generator

## What I Did
I containerized the QR Code Generator Python application by writing a secure and efficient Dockerfile using a slim Python base image. The container installs dependencies from requirements.txt, runs as a non-root user, and generates QR codes for any provided URL.

## Challenges Faced
- Understanding Docker layers and caching to speed up builds.
- Fixing permission issues when running the app as a non-root user.
- Ensuring Pillow and qrcode libraries built correctly on a slim image.

## Key Learnings
- Always use `COPY requirements.txt` before copying source files for efficient Docker caching.
- Running containers as non-root users is a simple but crucial security improvement.
- Automating builds and pushes using GitHub Actions and DockerHub tokens saves time and prevents human error.

## Next Steps
- Add automated tests before the build step.
- Use Docker multi-stage builds to reduce image size further.
