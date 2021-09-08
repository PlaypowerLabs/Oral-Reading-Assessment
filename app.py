import streamlit as st
from record import Sound
from passage_list import ENGLISH_PASSAGE_LIST, HINDI_PASSAGE_LIST
from settings import WAVE_OUTPUT_FILE
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch
import librosa
import jiwer
import random

def get_passage(language):
    if language == 'English':
        passage = random.choice(ENGLISH_PASSAGE_LIST)
    elif language == 'Hindi':
        passage = random.choice(HINDI_PASSAGE_LIST)

    return passage

@st.cache(allow_output_mutation=True, show_spinner=False)
def load_model(language):
    if language == 'English':
        processor = Wav2Vec2Processor.from_pretrained('models/wav2vec2-indian-english')
        model = Wav2Vec2ForCTC.from_pretrained('models/wav2vec2-indian-english')
    
    elif language == 'Hindi':
        processor = Wav2Vec2Processor.from_pretrained('models/wav2vec2-hindi')
        model = Wav2Vec2ForCTC.from_pretrained('models/wav2vec2-hindi')
    
    return processor, model

@st.cache(allow_output_mutation=True, show_spinner=False)
def load_eng_spell_checker():
    from neuspell import BertChecker
    checker = BertChecker()
    checker.from_pretrained('models/subwordbert-probwordnoise')
    return checker

def parse_transcription(wav_file, processor, model, checker = None):
    audio_input, sample_rate = librosa.load(wav_file, sr=16000)
    input_values = processor(audio_input, sampling_rate=16_000, return_tensors="pt").input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1).squeeze()
    softmax_probs = torch.nn.Softmax(dim=-1)(logits)
    seq_prob = torch.max(softmax_probs, dim=-1).values.squeeze()
    rem_tokens = [0,1,2,3,4]
    seq_prob = seq_prob[[(token not in rem_tokens) for token in predicted_ids]]
    confidence = (torch.prod(seq_prob)**(1/len(seq_prob))).item()

    transcription = processor.decode(predicted_ids, skip_special_tokens=True)
    if checker is not None:
        transcription = checker.correct(transcription)
    return confidence, transcription


def get_results(ground_truth_passage, transcription):
    
    transformation = jiwer.Compose([
                                jiwer.ToLowerCase(),
                                jiwer.RemovePunctuation(),
                                jiwer.RemoveWhiteSpace(replace_by_space=True),
                                jiwer.RemoveMultipleSpaces(),
                                jiwer.Strip(),
                                jiwer.SentencesToListOfWords(),
                                jiwer.RemoveEmptyStrings()
])

    metrics = jiwer.compute_measures(ground_truth_passage, transcription, truth_transform=transformation, hypothesis_transform=transformation)

    audio_dur = librosa.get_duration(filename=WAVE_OUTPUT_FILE)
    n_words = len(transcription.split())
    wpm = (60*n_words)/audio_dur
    return metrics['wer'],wpm


def main():
    
    st.title('Oral Reading Assessment')

    if 'show_passage_val' not in st.session_state:
        st.session_state.show_passage_val = False
    
    if 'language_val' not in st.session_state:
        st.session_state.language_val = ''
    
    if st.session_state.show_passage_val == False:

        language = st.selectbox('Select Language', options=('English','Hindi'))
        st.session_state.language_val = language

        if st.button('Show Passage'):
            st.session_state.show_passage_val = True
            st.experimental_rerun()
    
    if st.session_state.show_passage_val:

        if 'first_show_passage' not in st.session_state:
            st.session_state.first_show_passage = False
        
        if 'ground_truth_passage' not in st.session_state:
            st.session_state.ground_truth_passage = ''
        
        with st.spinner('Loading....'):

            processor, model = load_model(st.session_state.language_val)

            if st.session_state.language_val == 'English':
                checker = load_eng_spell_checker()

        passage = st.empty()

        if st.session_state.first_show_passage == False:
            st.session_state.ground_truth_passage = get_passage(st.session_state.language_val)
            st.session_state.first_show_passage = True

        if st.button('Change Passage') and st.session_state.first_show_passage:
            st.session_state.ground_truth_passage = get_passage(st.session_state.language_val)

        passage.write(st.session_state.ground_truth_passage)

        if st.button('Record'):
            with st.spinner('Recording in Progress....'):
                sound=Sound()
                sound.record_audio()
            st.success('Recorded Successfully')

            with st.spinner('Transcribing Audio....'):
                if st.session_state.language_val == 'English':
                    confidence, transcription = parse_transcription(WAVE_OUTPUT_FILE, processor, model, checker)
                else:
                    confidence, transcription = parse_transcription(WAVE_OUTPUT_FILE, processor, model)
            st.success('Audio Transcribed Successfully')

            with st.spinner('Computing Results....'):
                wer,wpm = get_results(st.session_state.ground_truth_passage, transcription)
            st.success('Results Computed Successfully')

            st.write('## **RESULTS**')
            st.write('**Transcribed Audio :**', transcription)
            st.write('**Word Error Rate :**', round(wer*100,2))
            st.write('**Words Per Minute :**', round(wpm,0))
            st.write('**Confidence:**', round(confidence*100,2))

            


        
        if st.button('Play'):
            try:
                
                audio_file = open(WAVE_OUTPUT_FILE,'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/wav')
            
            except:
                st.write('Please record audio sound first')

    


if __name__ == '__main__':
    main()