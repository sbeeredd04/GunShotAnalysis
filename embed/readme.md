Here's a comprehensive `README.md` file that provides clear documentation on how the system works, what each part does, and how to use it. This documentation explains the setup, purpose, and functionality of both `record_audio.py` and `processor.py`.

### README.md

```markdown
# Real-Time Audio Peak Detection System

This project provides a real-time audio peak detection system using Python. The system records audio in 5-second chunks, converts the audio data to a Bark scale spectrogram, and detects peaks in the audio signal. It utilizes PyAudio for audio input and `librosa` for processing the audio spectrogram.

## Table of Contents

1. [Overview](#overview)
2. [Requirements](#requirements)
3. [File Descriptions](#file-descriptions)
4. [How It Works](#how-it-works)
5. [Running the Program](#running-the-program)
6. [Configuration](#configuration)
7. [Additional Notes](#additional-notes)

---

## Overview

The system continuously records audio, divides it into 5-second chunks, and processes each chunk in real-time to detect prominent peaks in the audio signal. This setup uses two files:

- `record_audio.py`: Handles recording audio and queues each 5-second chunk for processing.
- `processor.py`: Processes each chunk, converts it to a Bark scale spectrogram, and identifies peaks in the signal.

The peaks are detected based on their prominence, allowing users to understand specific patterns or identify strong frequency components in the audio data.

## Requirements

- **Python** 3.6 or later
- **Libraries**:
  - `pyaudio`: For recording audio in real-time.
  - `librosa`: For audio processing and generating the spectrogram.
  - `numpy`: For efficient handling of audio data arrays.
  - `scipy`: For peak detection in the spectrogram.

To install the required packages, you can run:
```bash
pip install pyaudio librosa numpy scipy
```

## File Descriptions

### 1. `record_audio.py`

- **Purpose**: Continuously records audio from the microphone, accumulates it in 5-second chunks, and sends each chunk to a queue for processing.
- **Main Components**:
  - **Audio Configuration**: Sets the sample rate, format, and chunk size for audio recording.
  - **`record_audio` Function**: Collects 0.5-second chunks and combines them into 5-second segments. Each 5-second segment is added to a queue.
  - **`process_audio_chunks` Function**: Retrieves each 5-second chunk from the queue and processes it using `processor.py` to detect peaks.
  - **Parallel Processing**: Uses multiprocessing to run recording and processing concurrently, ensuring real-time performance.

### 2. `processor.py`

- **Purpose**: Processes each 5-second audio chunk, converts it to a Bark scale spectrogram, and detects prominent peaks.
- **Main Components**:
  - **`hz_to_bark` Function**: Converts frequency values to the Bark scale, commonly used in psychoacoustics.
  - **`process_audio_chunk` Function**: Accepts an audio chunk, generates a spectrogram, and identifies peaks.
  - **`find_peaks_and_return_details` Function**: Calculates decibel levels over specified buffered intervals and identifies peaks based on prominence.

## How It Works

1. **Audio Recording**: `record_audio.py` records audio in real-time using PyAudio. Audio data is collected in 0.5-second chunks and accumulated into 5-second segments.
2. **Queueing**: Each 5-second audio chunk is placed in a multiprocessing queue.
3. **Audio Processing**: `processor.py` processes each 5-second audio segment by:
   - Converting the audio data to a Short-Time Fourier Transform (STFT) spectrogram.
   - Calculating the Bark scale frequencies.
   - Detecting prominent peaks in the averaged decibel levels across a specified buffering interval.
4. **Peak Detection Output**: The program outputs the detected peaks with details such as time, frequency, and decibel values for each peak.

## Running the Program

To start the real-time peak detection system, simply run `record_audio.py`:
```bash
python record_audio.py
```

### Expected Output

The program will continuously display the detected peaks for each 5-second audio segment in the following format:
```
Detected Peaks: [{'time': 1.27, 'frequencies': [...], 'decibels': [...]}, ...]
```
Each detected peak will include:
- `time`: Timestamp of the peak within the 5-second segment.
- `frequencies`: List of Bark scale frequencies at the time of the peak.
- `decibels`: Corresponding decibel levels for each frequency at the peak time.

## Configuration

The audio configuration parameters can be adjusted as needed:

- **Sample Rate (`RATE`)**: Adjust to match the desired quality. Common values are 44100 Hz (high quality) and 22050 Hz (standard quality).
- **Buffer Duration (`BUFFER_DURATION`)**: Defines the length of audio to be processed at once. Currently set to 5 seconds.
- **Buffer Frame Duration (`buffer_ms`)**: Sets the averaging interval for decibel levels, in milliseconds, for peak detection.

To modify these parameters, update the corresponding values in the `record_audio.py` or `processor.py` files.

## Additional Notes

- **Concurrent Processing**: This system uses Python's multiprocessing to enable real-time processing without blocking audio recording. Recording and processing run in parallel.
- **Prominence-based Peak Detection**: The peaks are identified based on prominence in the decibel spectrogram. Adjust the `prominence` parameter in `processor.py` for different sensitivity levels.
- **Bark Scale**: The Bark scale is used for frequency analysis to reflect human hearing more accurately, especially useful in audio signal analysis.

## Troubleshooting

- **Audio Device Issues**: If you encounter issues with `pyaudio`, ensure your input device (e.g., microphone) is set up correctly on your system.
- **Import Errors**: Ensure all dependencies (`pyaudio`, `librosa`, `numpy`, `scipy`) are installed as per the requirements section.
