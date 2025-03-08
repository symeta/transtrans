from flask import Flask, render_template
import pyaudio
import threading
import asyncio
from flask_socketio import SocketIO
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent
import boto3  # 添加这行来支持Amazon Translate
from flask import request, jsonify

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# 全局变量
recording = False
audio_stream = None
transcription_thread = None
translate_client = boto3.client('translate', region_name='us-east-1')  # 添加translate客户端

class MyEventHandler(TranscriptResultStreamHandler):
    def __init__(self, transcript_result_stream, source_lang_code, target_lang_code):
        super().__init__(transcript_result_stream)
        self.last_result = ""
        self.source_lang_code = source_lang_code
        self.target_lang_code = target_lang_code

    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        results = transcript_event.transcript.results
        if len(results) > 0 and results[0].is_partial == False:
            transcript = results[0].alternatives[0].transcript
            if transcript != self.last_result:
                self.last_result = transcript
                
                try:
                    # 调用Amazon Translate进行翻译
                    translation_response = translate_client.translate_text(
                        Text=transcript,
                        SourceLanguageCode=self.source_lang_code.split('-')[0],  # 转换语言代码格式
                        TargetLanguageCode=self.target_lang_code
                    )
                    translated_text = translation_response['TranslatedText']
                    
                    print(f"\r原文: {transcript}", flush=True)
                    print(f"\r译文: {translated_text}", flush=True)
                    print("-" * 50)
                      
                    socketio.emit('transcription_update', {
                        'source': transcript,
                        'target': translated_text
                    })
                except Exception as e:
                    print(f"翻译错误: {str(e)}")
                    socketio.emit('transcription_update', {
                        'source': transcript,
                        'target': "Translation error"
                    })

class AudioStream:
    def __init__(self):
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.p = pyaudio.PyAudio()
        
        # 列出所有可用的音频输入设备
        self.list_audio_devices()
        
        # 选择BlackHole作为输入设备
        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            input_device_index=self.get_blackhole_device_index(),  # 获取BlackHole设备索引
            frames_per_buffer=self.chunk
        )
        print("音频捕获已启动...")

    def list_audio_devices(self):
        """列出所有可用的音频设备"""
        print("\n可用的音频输入设备:")
        for i in range(self.p.get_device_count()):
            device_info = self.p.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:  # 只显示输入设备
                print(f"设备索引 {i}: {device_info['name']}")

    def get_blackhole_device_index(self):
        """获取BlackHole设备的索引"""
        for i in range(self.p.get_device_count()):
            device_info = self.p.get_device_info_by_index(i)
            # 根据实际的BlackHole设备名称进行匹配
            if 'BlackHole' in device_info['name']:
                return i
        raise Exception("未找到BlackHole音频设备")

    def read_audio(self):
        return self.stream.read(self.chunk, exception_on_overflow=False)
    
    def close(self):
        if hasattr(self, 'stream') and self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if hasattr(self, 'p') and self.p:
            self.p.terminate()
        print("音频流已关闭")

async def transcribe_audio(source_lang_code, target_lang_code):
    global recording, audio_stream
    
    client = TranscribeStreamingClient(region="us-east-1")
    
    stream = await client.start_stream_transcription(
        language_code=source_lang_code,
        media_sample_rate_hz=16000,
        media_encoding="pcm",
    )
    
    handler = MyEventHandler(stream.output_stream, source_lang_code, target_lang_code)
    process_task = asyncio.create_task(handler.handle_events())
    
    audio_stream = AudioStream()
    
    try:
        print("转录服务已启动...")
        while recording:
            audio_chunk = audio_stream.read_audio()
            await stream.input_stream.send_audio_event(audio_chunk=audio_chunk)
            await asyncio.sleep(0.001)
    
    except Exception as e:
        print(f"\n转录过程中发生错误: {str(e)}")
    finally:
        await stream.input_stream.end_stream()
        await process_task
        if audio_stream:
            audio_stream.close()
            audio_stream = None
        print("转录服务已结束")

def run_transcription():
    asyncio.run(transcribe_audio())

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_transcription', methods=['POST'])
def start_transcription():
    global recording, transcription_thread
    
    if not recording:
        data = request.json
        source_lang_code = data.get('sourceLanguage', 'zh-CN')
        print("~~~~~~~~~~~~~~~~~~")
        print(source_lang_code)
        target_lang_code = data.get('targetLanguage', 'en')
        print(target_lang_code)
        
        recording = True
        transcription_thread = threading.Thread(
            target=lambda: asyncio.run(transcribe_audio(source_lang_code, target_lang_code))
        )
        transcription_thread.daemon = True
        transcription_thread.start()
        return {"status": "success", "message": "转录已启动"}
    return {"status": "error", "message": "转录已在进行中"}

@app.route('/stop_transcription', methods=['POST'])
def stop_transcription():
    global recording, transcription_thread, audio_stream
    
    if recording:
        recording = False
        if transcription_thread:
            transcription_thread.join(timeout=2)
            transcription_thread = None
        if audio_stream:
            audio_stream.close()
            audio_stream = None
        return {"status": "success", "message": "转录已停止"}
    return {"status": "error", "message": "转录未在进行"}

if __name__ == '__main__':
    socketio.run(app, debug=True)
