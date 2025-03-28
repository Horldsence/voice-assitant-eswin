from vosk import Model, KaldiRecognizer
import pyaudio

def vosk_recognize():
    # 下载中文模型: https://alphacephei.com/vosk/models
    model = Model("model/vosk-model-small-zh-cn-0.22")  # 替换为你的模型路径
    
    recognizer = KaldiRecognizer(model, 16000)
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, 
                     rate=16000, input=True, frames_per_buffer=8192)
    
    print("开始录音(按Ctrl+C停止)...")
    try:
        while True:
            data = stream.read(4096)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                print("识别结果:", result)
    except KeyboardInterrupt:
        print("停止录音")
    finally:
        stream.stop_stream()
        stream.close()
        mic.terminate()

vosk_recognize()