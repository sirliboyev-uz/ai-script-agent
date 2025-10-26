## Development Guide

### Project Structure

```
ai-script-agent/
├── src/
│   ├── agents/              # Claude AI agents
│   │   ├── base.py          # Base agent with Claude SDK
│   │   ├── researcher.py    # Research & synthesis agent
│   │   └── scriptwriter.py  # Script generation agent
│   ├── api/                 # API-related code (reserved)
│   ├── models/              # Database models & schemas
│   │   ├── database.py      # SQLAlchemy models
│   │   └── schemas.py       # Pydantic schemas
│   ├── services/            # Business logic
│   │   └── script_service.py # Script generation workflow
│   ├── utils/               # Utilities
│   │   ├── exceptions.py    # Custom exceptions
│   │   └── validators.py    # Input validation
│   ├── templates/           # HTML templates
│   │   └── index.html       # Frontend interface
│   ├── config.py            # Configuration management
│   └── main.py              # FastAPI application
├── tests/                   # Test files (future)
├── data/                    # SQLite database storage
├── requirements.txt         # Python dependencies
├── .env.example             # Environment template
├── setup.sh                 # Setup script
└── test_setup.py            # Setup verification

### Architecture

**Flow:**
1. User submits topic via web interface
2. API validates input and creates database record
3. ResearchAgent gathers information using Claude
4. ScriptwriterAgent generates YouTube script
5. Results saved to database and returned to user

**Components:**

**ClaudeAgent (base.py)**
- Handles Claude API communication
- Manages tool use and token tracking
- Provides unified interface for all agents

**ResearchAgent (researcher.py)**
- Conducts topic research
- Synthesizes findings from multiple perspectives
- Extracts key facts, statistics, and sources
- Returns structured research data

**ScriptwriterAgent (scriptwriter.py)**
- Generates YouTube-optimized scripts
- Structures content (hook, intro, body, conclusion)
- Applies brand voice guidelines
- Optimizes for engagement and retention

**ScriptService (script_service.py)**
- Orchestrates research → script workflow
- Validates inputs and outputs
- Manages database persistence
- Handles error recovery

### Database Schema

**Script Model:**
- `script_id`: Unique identifier (UUID)
- `topic`: Video topic input
- `style`: Script style (educational/entertaining/inspirational)
- `duration`: Target video duration
- `research_data`: JSON research findings
- `sources`: JSON source citations
- `title`: Generated video title
- `description`: SEO description
- `keywords`: Array of keywords
- `full_script`: Complete script text
- `script_sections`: JSON structured sections
- `estimated_duration`: Calculated duration
- `tone`: Script tone
- `target_audience`: Audience description
- `tokens_used`: Total API tokens consumed
- `generation_time`: Processing time in seconds
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### API Endpoints

**GET /**
- Serves frontend interface
- Returns: HTML page

**GET /health**
- Health check
- Returns: JSON status

**POST /api/generate**
- Generate script from topic
- Body: `{topic, style?, duration?, research_depth?, brand_voice?}`
- Returns: Complete script data

**GET /api/scripts/{script_id}**
- Retrieve script by ID
- Returns: Script data

**GET /api/scripts**
- List all scripts (paginated)
- Query: `?skip=0&limit=10`
- Returns: `{total, scripts[]}`

### Configuration

**Environment Variables (.env):**
```bash
ANTHROPIC_API_KEY=sk-ant-...        # Required
DEBUG=true                          # Optional (default: false)
HOST=0.0.0.0                        # Optional (default: 0.0.0.0)
PORT=8000                           # Optional (default: 8000)
DATABASE_URL=sqlite+aiosqlite:///./data/scripts.db  # Optional
```

**Settings (config.py):**
- `CLAUDE_MODEL`: claude-3-5-sonnet-20241022
- `MAX_TOKENS`: 4096
- Validates required configuration on startup

### Error Handling

**Custom Exceptions:**
- `ValidationError`: Input validation failures
- `ResearchError`: Research phase failures
- `ScriptGenerationError`: Script generation failures
- `ConfigurationError`: Config/setup issues

**Validation:**
- Topic: 5-500 characters, no spam patterns
- Style: Must be educational|entertaining|inspirational
- Duration: Predefined options only
- Research depth: quick|medium|deep
- Brand voice: Max 1000 characters

### Development Workflow

**Setup:**
```bash
# Run setup script
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key
```

**Run Tests:**
```bash
python test_setup.py
```

**Start Development Server:**
```bash
# Method 1: Direct
python -m src.main

# Method 2: Uvicorn with reload
uvicorn src.main:app --reload

# Method 3: Custom host/port
uvicorn src.main:app --host 0.0.0.0 --port 3000 --reload
```

**Access Application:**
- Frontend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

### Testing

**Manual Testing:**
1. Open http://localhost:8000
2. Enter topic: "How to start a YouTube channel"
3. Select style, duration, research depth
4. Click "Generate Script"
5. Wait 30-60 seconds
6. Review generated script
7. Check database: `sqlite3 data/scripts.db "SELECT * FROM scripts;"`

**API Testing:**
```bash
# Generate script
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "How to learn programming",
    "style": "educational",
    "duration": "10-15 minutes",
    "research_depth": "medium"
  }'

# List scripts
curl http://localhost:8000/api/scripts

# Get specific script
curl http://localhost:8000/api/scripts/{script_id}
```

### Performance

**Expected Metrics:**
- Research phase: 10-20 seconds
- Script generation: 15-30 seconds
- Total time: 30-60 seconds per script
- Token usage: 3K-8K tokens per generation
- Cost per script: ~$0.05-0.15

**Optimization Tips:**
- Use "quick" research depth for faster results
- Cache common topics to avoid re-research
- Implement rate limiting for production
- Consider async processing for bulk requests

### Future Enhancements

**Phase 2 - Improvements:**
- [ ] Add caching layer for research results
- [ ] Implement script editing/refinement endpoint
- [ ] Add YouTube API integration for metadata optimization
- [ ] Create script templates library
- [ ] Add multi-language support

**Phase 3 - Advanced Features:**
- [ ] Voice tone analysis and matching
- [ ] Competitor script analysis
- [ ] SEO optimization suggestions
- [ ] Thumbnail text recommendations
- [ ] Video chapter generation

**Phase 4 - Integrations:**
- [ ] Notion API for workspace export
- [ ] Google Sheets integration
- [ ] n8n workflow automation
- [ ] Pictory.ai video generation
- [ ] YouTube upload automation

**Phase 5 - Commercialization:**
- [ ] User authentication & authorization
- [ ] Subscription/pricing tiers
- [ ] Usage analytics dashboard
- [ ] Team collaboration features
- [ ] API access for third-party integrations

### Troubleshooting

**Common Issues:**

1. **"ANTHROPIC_API_KEY is required"**
   - Edit .env file and add your API key
   - Ensure no spaces around = in .env

2. **Import errors**
   - Activate virtual environment: `source venv/bin/activate`
   - Install dependencies: `pip install -r requirements.txt`

3. **Database errors**
   - Ensure data/ directory exists
   - Check file permissions
   - Delete data/scripts.db and restart

4. **Port already in use**
   - Change PORT in .env
   - Or kill process: `lsof -ti:8000 | xargs kill`

5. **Slow generation**
   - Use "quick" research depth
   - Check internet connection
   - Verify API key is valid

### Contributing

**Code Style:**
- Follow PEP 8
- Use type hints
- Add docstrings to all functions
- Keep functions focused and small

**Commit Messages:**
- feat: New feature
- fix: Bug fix
- docs: Documentation
- refactor: Code restructuring
- test: Testing additions

### License

MIT License - See LICENSE file
