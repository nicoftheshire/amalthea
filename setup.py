from setuptools import find_packages, setup

setup(
    name="sentiment_pipeline",
    packages=find_packages(exclude=["sentiment_pipeline_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-webserver",
        "newsapi",
        "textblob",
        "pyarrow",
        "pandas",
        "numpy",
        "transformers",
        "torch",
        "requests",
        "beautifulsoup4",
        "langdetect",
        "spacy",
        "sentencepiece",
        "sacremoses"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
