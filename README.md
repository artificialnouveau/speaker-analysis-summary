# Audio Conversation Analyzer

## Overview
This Python application analyzes an audio file, identifies unique speakers in the conversation, and summarizes the conversation both as a whole and per speaker. It also has an option to create word clouds for the entire conversation and for individual speakers.

## Dependencies
- Python 3.6+
- pyAudioAnalysis
- openai-whisper
- pydub
- matplotlib
- wordcloud
- transformers (for the summarizer)
- torch (for the summarizer)

You can install these packages using pip:
```bash
pip install pyAudioAnalysis openai-whisper pydub matplotlib wordcloud transformers torch
```

## How to Run
1. Update the `audio_file` variable in the `if __name__ == "__main__":` section of the script to the path of your audio file.
2. Run the script using Python:
```bash
python audio_analysis.py
```

## Functionality

### Speaker Diarization
This script uses pyAudioAnalysis's speaker diarization functionality to separate the conversation into segments by speaker.

### Speech-to-Text
Each segment from the speaker diarization is transcribed to text using OpenAI's Whisper ASR system.

### Text Summarization
The transcript for each speaker segment, as well as the entire conversation, is summarized using a BERT-based text summarizer.

### Word Clouds
Optionally, the script can generate a word cloud for each speaker segment and for the entire conversation. The word clouds are displayed as plots.

## Output
The script prints the summary of the conversation for each speaker and optionally displays the word clouds.
