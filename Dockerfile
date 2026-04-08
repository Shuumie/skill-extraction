FROM ollama
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY SkillExtraction /app/SkillExtraction

RUN useradd app
USER app

CMD [ "python", "SkillExtraction/OllamaSkillExtraction.py" ]