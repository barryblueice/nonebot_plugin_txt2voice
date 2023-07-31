from nonebot import on_command
from nonebot.adapters.onebot.v11 import *
from utils.utils import scheduler
import pyttsx3
import os
# from operator import length_hint

__zx_plugin_name__ = "语音转换"
__plugin_des__ = "语音转换"
__plugin_type__ = ("一些工具",)
__plugin_cmd__ = ["/speak"]
__plugin_settings__ = {
    "level": 1,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["/speak"],
}

save_path = ""

def pyttsx3_debug(text,language,rate,volume,filename):
    
    engine = pyttsx3.init() 
    engine.setProperty('rate', rate) 
    engine.setProperty('volume', volume)
    voices = engine.getProperty('voices')  # 获取当前语音的详细信息
    if int(language)==0:
        engine.setProperty('voice', voices[0].id)  # 设置第一个语音合成器 #改变索引，改变声音。0中文,1英文(只有这两个选择)
    elif int(language)==1:
        engine.setProperty('voice', voices[1].id)
    engine.save_to_file(text, (save_path+filename+'.mp3'))
    engine.runAndWait() # pyttsx3结束语句(必须加)
    engine.stop()

speak = on_command("/speak",block=True, priority=5)
@speak.handle()
async def process(bot: Bot, event: MessageEvent):

    if not os.path.exists(save_path.rstrip('/')):
        os.makedirs(save_path.rstrip('/'))
    file_list = os.listdir(save_path)
    speak_buffer = str(event.get_message()).strip()+"             "
    filename = speak_buffer.strip('/speak').lstrip().replace(" ","")
    if (filename+'.mp3') not in file_list:
        await speak.send("正在合成中（如若文本较长则生成时间较长，请耐心等待）")
        pyttsx3_debug(text=speak_buffer,language=0,rate=170,volume=0.9,filename=filename)
        msg = f"[CQ:tts,text={filename}]"
        await speak.finish(Message(msg))
    else:
        msg = f"[CQ:tts,text={filename}]"
        await speak.finish(Message(msg))

    
    

