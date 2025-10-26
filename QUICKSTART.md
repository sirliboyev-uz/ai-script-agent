# Quick Start Guide

## Prerequisites

- Python 3.9 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

## Installation

### Option 1: Automated Setup (Recommended)

```bash
./setup.sh
```

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create environment file
cp .env.example .env

# 5. Edit .env and add your API key
nano .env  # or use your preferred editor
```

## Configuration

Edit `.env` file:

```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here  # Required
DEBUG=true                               # Optional
HOST=0.0.0.0                            # Optional
PORT=8000                               # Optional
```

## Verify Setup

```bash
python test_setup.py
```

You should see:
```
🎉 All tests passed! Your setup is ready.
```

## Run the Application

```bash
# Start the server
uvicorn src.main:app --reload

# OR
python -m src.main
```

## Access the Application

1. Open your browser: http://localhost:8000
2. Enter a video topic (e.g., "How to start a YouTube channel")
3. Click "Generate Script"
4. Wait 30-60 seconds
5. Review your AI-generated script!

## API Usage

### Generate a Script

```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "How to learn Python programming",
    "style": "educational",
    "duration": "10-15 minutes",
    "research_depth": "medium"
  }'
```

### List All Scripts

```bash
curl http://localhost:8000/api/scripts
```

### Get Specific Script

```bash
curl http://localhost:8000/api/scripts/{script_id}
```

## Example Topics to Try

- "How to start a dropshipping business"
- "Best practices for remote work"
- "Introduction to machine learning"
- "Healthy meal prep for beginners"
- "Photography tips for beginners"

## Troubleshooting

### Dependencies Not Installed
```bash
pip install -r requirements.txt
```

### API Key Error
Make sure your `.env` file contains a valid `ANTHROPIC_API_KEY`

### Port Already in Use
Change the `PORT` in `.env` to a different number (e.g., 3000)

### Database Errors
```bash
rm -rf data/scripts.db
python -m src.main
```

## Next Steps

- Read `DEVELOPMENT.md` for detailed documentation
- Check `README.md` for API reference
- Explore the code in `src/` directory

## Support

- Report issues: Create an issue on GitHub
- Questions: Check DEVELOPMENT.md for details

---

Enjoy creating AI-powered YouTube scripts! 🎬
