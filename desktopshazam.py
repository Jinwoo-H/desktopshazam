import soundcard as sc
import soundfile as sf
import os
from pydub import AudioSegment
import asyncio
from shazamio import Shazam


def audioCapture(file_name): #Desktop audio to wav code by tez3998
    
    OUTPUT_FILE_NAME = f"{file_name}.wav"    # file name.
    SAMPLE_RATE = 48000              # [Hz]. sampling rate.
    RECORD_SEC = 5                  # [sec]. duration recording audio.

    with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
        # record audio with loopback from default speaker.
        data = mic.record(numframes=SAMPLE_RATE*RECORD_SEC)
        
        sf.write(file=OUTPUT_FILE_NAME, data=data[:, 0], samplerate=SAMPLE_RATE)

    #Convert wav to ogg 
    AudioSegment.from_wav(f"{file_name}.wav").export(f"{file_name}.ogg", format="ogg") 
    os.remove(f"{file_name}.wav")
    # asyncio.run(recognizeSong(file_name))
    
    asyncio.run(recognizeSong(file_name))
    # recognizeSong(file_name)

async def recognizeSong(file_name):
    shazam = Shazam()
    out = await shazam.recognize_song(f'{file_name}.ogg')
    print('Song: ' + out['track']['title'] + ', by: ' + out['track']['subtitle'])

    loop = asyncio.get_event_loop()
    loop.run_until_complete(recognizeSong(file_name))

audioCapture("outputs")
