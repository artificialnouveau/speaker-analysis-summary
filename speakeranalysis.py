import os
import matplotlib.pyplot as plt
from pyAudioAnalysis import audioSegmentation as aS
from summarizer import Summarizer
from pydub import AudioSegment
import whisper
from wordcloud import WordCloud

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
    
    speaker_summaries = []
    all_text = []

    # Convert seconds to milliseconds for pydub
    speaker_segments = [(seg[0]*1000, seg[1]*1000) for seg in speaker_segments]

    # Load audio file
    audio = AudioSegment.from_wav(audio_file)
    
    # Step 2 & 3: For each speaker segment, transcribe and summarize
    for i, segment in enumerate(speaker_segments):
        start, end = segment
        speaker_audio = audio[start:end]
        speaker_audio.export("temp.wav", format="wav")
        
        # Speech to Text
        transcript = get_transcript("temp.wav")
        all_text.append(transcript)
        
        # Text Summarization
        summary = summarize_text(transcript)
        speaker_summaries.append(summary)

        if word_cloud:
            generate_word_cloud(transcript, f"Speaker {i+1} Word Cloud")
    
    if word_cloud:
        generate_word_cloud(' '.join(all_text), "All Speakers Word Cloud")

    # Cleanup temporary file
    os.remove("temp.wav")

    return speaker_summaries, speaker_segments

if __name__ == "__main__":
    audio_file = os.path.join(os.getcwd(), 'audio_file.wav')  # Replace with your audio file path
    summaries, speakers = analyze_audio_file(audio_file, word_cloud=True)
    
    for i, summary in enumerate(summaries):
        print(f"Speaker {speakers[i]} summary: {summary}")
