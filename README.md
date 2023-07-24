# Speaker Analysis

This project provides a Python script to analyze audio files in various ways. It uses OpenAI's Whisper ASR system for speech-to-text, pyAudioAnalysis for speaker diarization, BERT-based Summarizer for text summarization, and the my-voice-analysis library for voice analysis. The script can also generate word clouds for each speaker's transcription.

## Getting Started

Ensure you have all necessary Python packages installed. You will need the following:

- OpenAI's Whisper ASR: Install the Python wrapper with `!pip install -U openai-whisper`.
- BERT-based Summarizer: Install with `pip install bert-extractive-summarizer`.
- pyAudioAnalysis: Install with `pip install pyAudioAnalysis`.
- pyDub: Install with `pip install pydub`.
- my-voice-analysis: Install with `pip install my-voice-analysis`.
- Matplotlib: Install with `pip install matplotlib`.
- WordCloud: Install with `pip install wordcloud`.

You will also need to install ffmpeg if you don't have it already: `apt install ffmpeg`.

## Usage

You can use this script by running it from the command line with the path to your audio file as an argument:

```bash
python script.py my_audio_file.wav
```

By default, the script will perform speaker diarization, transcription, text summarization, and voice analysis for each speaker, and output this data to JSON files (`sentences.json` and `summaries.json`). It will also perform these analyses for the entire conversation and include that in `summaries.json`.

You can also specify the `--word_cloud` argument to generate word clouds for each speaker's transcriptions:

```bash
python speakeranalysis.py my_audio_file.wav --word_cloud
```

Note: The script assumes 2 speakers in the audio file for diarization. You can change this by modifying the `n_speakers` argument in the `speaker_diarization` function.

## Output

The script outputs two JSON files:

1. `sentences.json`: Contains the transcriptions, speaker ID, and timestamp for each sentence.
2. `summaries.json`: Contains the summarized text and voice analysis data for each speaker, and for the entire conversation.

Each entry in `sentences.json` is in the following format:

```json
{
    "text": "transcription of sentence",
    "speaker": "speaker ID",
    "timestamp": [start time, end time]
}
```

Each entry in `summaries.json` (except for the 'Total' entry) is in the following format:

```json
"Speaker ID": {
    "summary": "summarized text",
    "voice_analysis": {
        "Gender recognition": gender,
        "Speech mood (semantic analysis)": mood,
        "Pronunciation posterior score": score,
        "Articulation-rate": rate,
        "Speech rate": rate,
        "Filler words": words
    }
}
```

The 'Total' entry in `summaries.json` contains the summarized text and voice analysis data for the entire conversation. The voice analysis data for the 'Total' entry is the analysis of the last speaker segment.

If you specify the `--word_cloud` argument, the script will also generate and display word clouds for each speaker's transcriptions.
