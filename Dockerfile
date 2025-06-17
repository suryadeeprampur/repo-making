
# Install ffmpeg
RUN apt update && apt install -y ffmpeg && apt clean

# Set working directory
WORKDIR /app

# Copy all bot files into the container
COPY . /app/

# Install required Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python3", "bot.py"]
