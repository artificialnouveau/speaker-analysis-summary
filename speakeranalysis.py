import os
import matplotlib.pyplot as plt
from pyAudioAnalysis import audioSegmentation as aS
from summarizer import Summarizer
from pydub import AudioSegment
import whisper
from wordcloud import WordCloud
import json
import myspsolution as mysp
# Import other necessary modules and functions

# Load models
summarizer_model = Summarizer()
whisper_model = whisper.load_model("base")

def get_transcript(audio_file):
    # Transcribe the audio file
    result = whisper_model.transcribe(audio_file)

    # Return the transcribed text
    return result["text"]

def speaker_diarization(audio_file):
    segments = aS.speaker_diarization(audio_file, n_speakers=2)  # Modify number of speakers accordingly
    return segments

def summarize_text(text):
    result = summarizer_model(text)
    return result

def generate_word_cloud(text, title):
    wordcloud = WordCloud().generate(text)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title(title)
    plt.show()

def analyze_audio_file(audio_file, word_cloud=False):
    # Step 1: Speaker Diarization
    speaker_segments = speaker_diarization(audio_file)

    # Convert seconds to milliseconds for pydub
    speaker_segments = [(seg[0]*1000, seg[1]*1000) for seg in speaker_segments]

    # Load audio file
    audio = AudioSegment.from_wav(audio_file)

    # Initialize results
    sentences = []
    speaker_summaries = {}

    # Step 2, 3, 4: For each speaker segment, transcribe, summarize and analyze voice
    for i, segment in enumerate(speaker_segments):
        start, end = segment
        speaker_audio = audio[start:end]
        speaker_audio.export("temp.wav", format="wav")

        # Speech to Text
        transcript = get_transcript("temp.wav")

        # Text Summarization
        summary = summarize_text(transcript)

        # Voice Analysis
        p = "temp.wav"
        c = "/content"  # Folder to save analysis outputs
        gender = mysp.myspgend(p, c)
        total = mysp.mysptotal(p, c)
        voice_data = {
            "Gender recognition": gender,
            "Speech mood (semantic analysis)": total['mood'],
            "Pronunciation posterior score": total['pronunciation_posterior_score'],
            "Articulation-rate": total['articulation_rate'],
            "Speech rate": total['speech_rate'],
            "Filler words": total['filler_words']
        }
        
        speaker_summaries[f"Speaker {i+1}"] = {
            'summary': summary,
            'voice_analysis': voice_data
        }

        # Add to sentences
        sentences.append({
            'text': transcript,
            'speaker': f"Speaker {i+1}",
            'timestamp': [start / 1000, end / 1000]  # Convert back to seconds
        })

        if word_cloud:
            generate_word_cloud(transcript, f"Speaker {i+1} Word Cloud")
    
    # Save sentences to JSON
    with open('sentences.json', 'w') as f:
        json.dump(sentences, f)

    # Add total summary to speaker_summaries and save to JSON
    speaker_summaries['Total'] = {
        'summary': summarize_text(' '.join([s['text'] for s in sentences])),
        'voice_analysis': voice_data  # Add voice analysis for the whole audio file
    }
    with open('summaries.json', 'w') as f:
        json.dump(speaker_summaries, f)

    # Cleanup temporary file
    os.remove("temp.wav")

    return sentences, speaker_summaries


if __name__ == "__main__":
    audio_file = os.path.join(os.getcwd(), 'audio_file.wav')  # Replace with your audio file path
    summaries, speakers = analyze_audio_file(audio_file, word_cloud=True)
    
    for i, summary in enumerate(summaries):
        print(f"Speaker {speakers[i]} summary: {summary}")
