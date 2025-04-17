# Use the official TensorFlow image as a base image.
FROM tensorflow/tensorflow:latest-gpu

# Set the working directory.
WORKDIR /app

# Copy the current directory contents into the container at /app (a requirements.txt file).
COPY . /app

# Install any needed packages specified in requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Install vscode server.
RUN curl -fsSL https://code-server.dev/install.sh | bash

# Add code-server to PATH
ENV PATH="/root/.local/bin:${PATH}"

# Expose the port that the server is running on.
EXPOSE 8080

# Run the code-server command when the container starts.
CMD ["code-server", "--auth", "none", "--bind-addr", "0.0.0.0:8080", "."]

