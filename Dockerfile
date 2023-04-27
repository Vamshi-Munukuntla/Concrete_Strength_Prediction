FROM python:3.7
COPY . /main
WORKDIR /main
RUN pip install -r requirements.txt
EXPOSE 8501
ENV STREAMLIT_SERVER_PORT=8501
CMD ["streamlit", "run", "main.py"]
