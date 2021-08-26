import streamlit as st
from record import Sound
from setup import PASSAGE_LIST,get_passage
from settings import WAVE_OUTPUT_FILE

def main():
    
    st.title('Oral Reading Assessment')

    if 'show_passage_val' not in st.session_state:
        st.session_state.show_passage_val = False
    
    if st.session_state.show_passage_val == False:
        if st.button('Show Passage'):
            st.session_state.show_passage_val = True
            st.experimental_rerun()
    
    if st.session_state.show_passage_val:

        if 'first_show_passage' not in st.session_state:
            st.session_state.first_show_passage = False
        
        if 'ground_truth_passage' not in st.session_state:
            st.session_state.ground_truth_passage = ''
        
        passage = st.empty()

        if st.session_state.first_show_passage == False:
            st.session_state.ground_truth_passage = get_passage()
            #st.write(ground_truth_passage)
            st.session_state.first_show_passage = True

        if st.button('Change Passage') and st.session_state.first_show_passage:
            st.session_state.ground_truth_passage = get_passage()
            #st.write(ground_truth_passage)

        passage.write(st.session_state.ground_truth_passage)

        if st.button('Record'):
            with st.spinner('Recording in Progress....'):
                sound=Sound()
                sound.record_audio()
            st.success('Recorded Successfully')
        
        if st.button('Play'):
            try:
                
                audio_file = open('input_audio.wav','rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/wav')
            
            except:
                st.write('Please record audio sound first')

    


if __name__ == '__main__':
    main()