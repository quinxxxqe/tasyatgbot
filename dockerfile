FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir aiogram aiohttp python-dotenv
EXPOSE 8080
CMD ["python", "bot.py"]
