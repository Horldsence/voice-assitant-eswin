import asyncio
import edge_tts
from pathlib import Path
from typing import Optional, Union

class TextToSpeech:
    """
    使用Edge-TTS实现文本转语音功能的类
    
    功能：
    - 文本转语音并保存为音频文件
    - 支持多种语音选项
    - 可调节语速和音量
    """
    
    def __init__(self):
        self.voices = asyncio.run(self._get_available_voices())
    
    async def _get_available_voices(self) -> list:
        """获取可用的语音列表"""
        return await edge_tts.list_voices()
    
    def list_voices(self, language: str = None, gender: str = None) -> list:
        """
        列出可用的语音选项
        
        参数:
            language: 语言代码 (如 'zh-CN', 'en-US')
            gender: 性别 ('Male' 或 'Female')
            
        返回:
            符合条件的语音列表
        """
        voices = self.voices
        if language:
            voices = [v for v in voices if language.lower() in v['ShortName'].lower()]
        if gender:
            voices = [v for v in voices if v['Gender'].lower() == gender.lower()]
        return voices
    
    async def text_to_speech(
        self,
        text: str,
        output_file: Union[str, Path],
        voice: str = "zh-CN-YunxiNeural",
        rate: str = "+0%",
        volume: str = "+0%",
    ) -> Optional[Path]:
        """
        将文本转换为语音并保存为音频文件
        
        参数:
            text: 要转换的文本
            output_file: 输出音频文件路径
            voice: 语音名称 (默认: 中文-云溪)
            rate: 语速调节 (如 "+10%", "-5%")
            volume: 音量调节 (如 "+10%", "-5%")
            
        返回:
            成功则返回保存的文件路径，失败返回None
        """
        try:
            output_path = Path(output_file).with_suffix('.mp3')
            communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate, volume=volume)
            
            # 确保输出目录存在
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 保存音频文件
            await communicate.save(output_path)
            
            print(f"语音文件已保存到: {output_path}")
            return output_path
        except Exception as e:
            print(f"文本转语音失败: {str(e)}")
            return None
    
    def tts_sync(
        self,
        text: str,
        output_file: Union[str, Path],
        voice: str = "zh-CN-YunxiNeural",
        rate: str = "+0%",
        volume: str = "+0%",
    ) -> Optional[Path]:
        """
        同步版本的文本转语音方法
        
        参数同 text_to_speech 方法
        """
        try:
            return asyncio.run(self.text_to_speech(text, output_file, voice, rate, volume))
        except Exception as e:
            print(f"同步文本转语音失败: {str(e)}")
            return None


# 使用示例
if __name__ == "__main__":
    tts = TextToSpeech()
    
    # 列出可用的中文语音
    print("可用的中文语音:")
    chinese_voices = tts.list_voices(language="zh-CN")
    for voice in chinese_voices:
        print(f"{voice['ShortName']} - {voice['Gender']}")
    
    # 文本转语音示例
    text = "大家好，这是一个使用Python实现的文本转语音示例。Edge-TTS提供了高质量的语音合成服务。"
    output_file = "output_audio.mp3"
    
    # 使用同步方法
    result = tts.tts_sync(
        text=text,
        output_file=output_file,
        voice="zh-CN-YunxiNeural",  # 中文男声
        rate="+10%",  # 加快10%语速
        volume="+0%"
    )
    
    if result:
        print(f"语音文件已成功生成: {result}")