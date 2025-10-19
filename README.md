# 🏏 Automated Cricket Commentary Video Generator

An end-to-end automated system that generates professional cricket commentary videos using AI avatars, dynamic charts, and intelligent video composition.

## 🎯 Features

- **AI-Powered Commentary**: Generate natural, engaging cricket commentary using Google Gemini
- **AI Avatar Videos**: Create realistic avatar commentary using HeyGen or D-ID
- **Dynamic Visualizations**: Automatic generation of cricket charts:
  - Run rate graphs
  - Manhattan charts (runs per over)
  - Wagon wheels (shot distribution)
  - Partnership progression
- **Professional Video Composition**: FFmpeg-powered video editing with transitions, overlays, and effects
- **Mock Mode**: Test the entire pipeline without API keys

## 📋 Prerequisites

### Required
- Python 3.8+
- FFmpeg (for video composition)

### Optional (for production)
- Google Gemini API key
- HeyGen API key OR D-ID API key

## 🚀 Installation

### 1. Install Python Dependencies
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install google-generativeai requests matplotlib numpy pillow
```

### 2. Install FFmpeg

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

#### macOS
```bash
brew install ffmpeg
```

#### Windows
Download from [ffmpeg.org](https://ffmpeg.org) and add to PATH

### 3. Set Up API Keys (Optional)
```bash
# For Gemini (script generation)
export GEMINI_API_KEY='your_gemini_api_key'

# For HeyGen (avatar videos)
export HEYGEN_API_KEY='your_heygen_api_key'


```

## 📁 Project Structure
```
cricket-commentary-generator/
├── cricket_script_generator.py      # Step 1: Commentary scripts
├── cricket_chart_generator.py       # Step 2: Chart generation
├── cricket_avatar_generator.py      # Step 3: Avatar videos
├── cricket_video_composer.py        # Step 4: Final composition
├── main.py                          # Main orchestrator
├── cricket_output/                  # Generated content
│   ├── charts/                      # Chart images
│   ├── avatar_videos/               # Avatar video clips
│   ├── scripts.json                 # Generated scripts
│   └── cricket_commentary_final.mp4 # Final video
└── temp_video_files/                # Temporary files
```

## 🎬 Quick Start

### Run the Complete Pipeline
```bash
python main.py
```

This will:
1. Generate commentary scripts (AI-powered)
2. Create cricket visualization charts
3. Generate AI avatar videos (API)
4. Compose final video with FFmpeg

### Run Individual Steps
```bash
# Step 1: Generate scripts only
python cricket_script_generator.py

# Step 2: Generate charts only
python cricket_chart_generator.py

# Step 3: Generate avatar videos only
python cricket_avatar_generator.py

# Step 4: Compose final video only
python cricket_video_composer.py
```

## 🔧 Configuration


### Using Real APIs

Edit `main.py` or set environment variables:
```python
config = {
    'gemini_api_key': 'your_key_here',
    'avatar_api_key': 'your_key_here',
    'avatar_provider': 'heygen',  # or 'd-id'
}
```

## 📊 Customization

### 1. Match Data

Edit `MOCK_MATCH_DATA` in `cricket_script_generator.py`:
```python
MOCK_MATCH_DATA = {
    "match_id": "IND_vs_PAK_2024_001",
    "teams": {
        "batting": "India",
        "bowling": "Pakistan"
    },
    "current_score": {
        "runs": 180,
        "wickets": 4,
        "overs": 30.0
    },
    # ... add more data
}
```

### 2. Commentary Style

Modify prompts in `CommentaryScriptGenerator._create_prompt()`:
```python
prompt = """You are an enthusiastic cricket commentator with a 
focus on exciting play-by-play commentary..."""
```

### 3. Chart Styling

Adjust colors and styles in `CricketChartGenerator`:
```python
self.colors = {
    'primary': '#00A8E8',
    'secondary': '#F4D03F',
    'accent': '#E74C3C',
    # ... customize colors
}
```

### 4. Video Layout

Modify composition in `VideoComposer.compose_segment()`:
```python
# Change avatar position, size, transition s, etc.
self.create_picture_in_picture(
    avatar_video, 
    chart_video, 
    output, 
    position="bottomright"  # Change  position
)
```

## 🎥 Sample Output

The generated video includes:
- **Segment 1 (0-25s)**: Match summary with run rate graph
- **Segment 2 (20-40s)**: Key moment highlight (avatar only)
- **Segment 3 (40-60s)**: Statistical analysis with Manhattan chart
- Professional transitions and overlays throughout

## 🔌 API Reference

### Gemini API
- **Purpose**: Generate natural commentary scripts
- **Get API Key**: [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Pricing**: Free tier available (60 requests/minute)

### HeyGen API
- **Purpose**: Create AI avatar videos
- **Get API Key**: [HeyGen Platform](https://app.heygen.com)
- **Pricing**: Paid service (~$0.15-0.30 per minute)
- **Docs**: [HeyGen API Docs](https://docs.heygen.com)

## 🐛 Troubleshooting

### FFmpeg Not Found
```bash
# Verify installation
ffmpeg -version

# If not found, reinstall or add to PATH
```

### Import Errors
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt  # Create this file if needed
```

### API Rate Limits

- **Gemini**: 60 requests/minute (free tier)
- **HeyGen**: Check your plan limits


Add delays between API calls if needed:
```python
import time
time.sleep(1)  # Wait 1 second between calls
```

### Video Quality Issues

Adjust FFmpeg settings in `VideoComposer`:
```python
self.video_codec = "libx264"  # Try h264, h265, etc.
self.fps = 30  # Increase for smoother video
```


## 📝 License

This project is provided as-is for educational and commercial use.

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional chart types (heatmaps, player comparisons)
- More avatar providers
- Real-time streaming support
- Multi-language commentary
- Advanced video effects

## 📧 Support

For issues and questions:
- Check troubleshooting section
- Review API documentation
- Open an issue on GitHub

## 🎓 Learning Resources

- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Google Gemini API Guide](https://ai.google.dev/docs)
- [HeyGen API Docs](https://docs.heygen.com)

---
