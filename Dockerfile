# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory and environment variable
WORKDIR /sentiment-pipeline
ENV DAGSTER_HOME=/sentiment-pipeline

# Install packages
RUN pip install --upgrade pip

# Install libraries that are unlikely to change frequently
RUN pip install --default-timeout=300 dagster dagster-webserver dagster-docker textblob newsapi pandas pyarrow requests beautifulsoup4 langdetect

# Install large language model libraries separately to avoid frequent reinstallation
RUN pip install --default-timeout=300 transformers torch spacy

# Install SentencePiece for language translation
RUN pip install --default-timeout=300 sentencepiece

RUN pip install --default-timeout=300 sacremoses

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Pre-download Hugging Face's Transformers models
RUN python -c "from transformers import AutoModelForSequenceClassification, AutoTokenizer; model_name = 'distilbert-base-uncased-finetuned-sst-2-english'; AutoModelForSequenceClassification.from_pretrained(model_name); AutoTokenizer.from_pretrained(model_name)"

# Pre-download MarianMT models
RUN python -c "from transformers import MarianMTModel, MarianTokenizer; MarianTokenizer.from_pretrained('Helsinki-NLP/opus-mt-de-en'); MarianMTModel.from_pretrained('Helsinki-NLP/opus-mt-de-en')"

# Download NLTK punkt tokenizer models
RUN python -m nltk.downloader punkt

# Copy code and workspace
COPY ./sentiment_pipeline/assets ./sentiment_pipeline/assets
COPY ./sentiment_pipeline_tests ./sentiment_pipeline_tests
COPY pyproject.toml .
COPY setup.cfg .
COPY setup.py .
COPY dagster.yaml .

# Set the working directory for CMD
WORKDIR /sentiment-pipeline/sentiment_pipeline/assets

# Expose port and set CMD
EXPOSE 3000
CMD [ "dagster", "dev", "-h", "0.0.0.0", "-p", "3000", "-f", "repository.py" ]
