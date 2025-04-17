# Themed IDE

A themed version of the Judge0 IDE.

## Prerequisites

- Docker
- Git

## Running the IDE

1. Clone the repository:
   ```bash
   git clone https://github.com/ianuriegas/themed-ide.git
   cd themed-ide
   ```

2. Build the Docker image:
   ```bash
   docker build -t themed-ide .
   ```

3. Run the container:
   ```bash
   docker run -p 8000:80 themed-ide
   ```

4. Navigate to the IDE in your browser:
   ```
   http://localhost:8000
   ```

## Development

For quick testing and development, you can use Python's built-in HTTP server:

```bash
cd ide
python3 -m http.server 8000
```

Then access the IDE at `http://localhost:8000`.

## Project Structure

- `ide/` - Contains the Judge0 IDE frontend code
- `Dockerfile` - Configuration for containerizing the IDE
- `.dockerignore` - Specifies files to exclude from the Docker build

## License

Based on [Judge0 IDE](https://github.com/judge0/ide) (MIT License)