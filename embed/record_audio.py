import pyaudio
import numpy as np
from multiprocessing import Queue, Process
from processor import process_audio_chunk  # Import function to process each chunk

# Audio Configuration
CHUNK = 22050  # 0.5 seconds if RATE is 44100 Hz
FORMAT = pyaudio.paFloat32  # 32-bit float format for audio data
CHANNELS = 1  # Mono channel recording
RATE = 44100  # Sample rate in Hz (samples per second)
CHUNK_DURATION = CHUNK / RATE  # Duration of each chunk in seconds
BUFFER_DURATION = 5  # Total duration of buffered audio for each processing cycle
BUFFER_CHUNKS = int(BUFFER_DURATION / CHUNK_DURATION)  # Number of chunks needed to reach 5 seconds


def record_audio(queue):
    p = pyaudio.PyAudio()
    try:
        # Open the audio stream with an exception handler for potential overflow
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        print("Recording audio...")
        
        buffer = []
        
        while True:
            try:
                # Read audio chunk
                audio_data = stream.read(CHUNK, exception_on_overflow=False)  # Handle overflow silently
                audio_np = np.frombuffer(audio_data, dtype=np.float32)
                print("[DEBUG] Read a 0.5-second chunk of audio data")

                # Collect chunks to reach 5 seconds (BUFFER_CHUNKS)
                buffer.append(audio_np)
                
                if len(buffer) >= BUFFER_CHUNKS:
                    # Combine chunks into a single 5-second buffer
                    audio_chunk = np.concatenate(buffer)
                    queue.put(audio_chunk)  # Add 5-second chunk to queue
                    print("[DEBUG] Added 5-second audio chunk to queue")
                    buffer = []  # Reset buffer to collect next 5-second chunk

            except OSError as e:
                print("[ERROR] Buffer overflow. Could not read audio data:", e)

    except Exception as e:
        print("[ERROR] Failed to open audio stream:", e)
    finally:
        if 'stream' in locals():
            stream.stop_stream()
            stream.close()
            print("[DEBUG] Stopped and closed audio stream")
        p.terminate()
        print("[DEBUG] Terminated PyAudio instance")


def process_audio_chunks(queue):
    while True:
        if not queue.empty():
            audio_chunk = queue.get()
            print("[DEBUG] Retrieved a 5-second audio chunk from the queue")
            
            # Process each 5-second chunk and print detected peaks
            peaks = process_audio_chunk(audio_chunk, RATE, buffer_ms=100)
            print("[DEBUG] Detected Peaks:", peaks)  # Display peaks for each chunk


if __name__ == "__main__":
    # Create a queue for audio chunks
    audio_queue = Queue()
    
    # Start recording process
    record_process = Process(target=record_audio, args=(audio_queue,))
    record_process.start()
    print("[DEBUG] Started audio recording process")
    
    # Start processing in parallel
    process_process = Process(target=process_audio_chunks, args=(audio_queue,))
    process_process.start()
    print("[DEBUG] Started audio processing process")
    
    record_process.join()
    process_process.join()
