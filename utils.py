from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper

import os

def generate_script(subject, video_length, creativity, api_key):
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "请为'{subject}'这个主题的视频想一个吸引人的标题")
        ]
    )
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human",
             """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
             视频标题：{title}，视频时长：{duration}分钟，脚本格式也请按照【标题、开头、中间，结尾】分隔。
             标题具体要求如下：
              一、标题创作技巧： 
                1. 采用二极管标题法进行标题创作 
                1.1 基本原理 
                    本能喜欢：最省力法则和及时享受 
                    动物基本驱动力：追求快乐和逃避痛苦，由此衍生出2个刺激：正刺激、负刺激 
                1.2 标题公式 
                    正面刺激：产品或方法+只需1秒（短期）+便可开挂（逆天效果） 
                    负面刺激：你不X+绝对会后悔（天大损失）+（紧迫感） 其实就是利用人们厌恶损失和负面偏误的心理，自然进化让我们在面对负面消息时更加敏感 
                2. 使用具有吸引力的标题 
                2.1 使用标点符号，创造紧迫感和惊喜感 
                2.2 采用具有挑战性和悬念的表述 
                2.3 利用正面刺激和负面刺激 
                2.4 融入热点话题和实用工具 
                2.5 描述具体的成果和效果 
                2.6 使用emoji表情符号，增加标题的活力 
                3. 使用爆款关键词 
                    从列表中选出1-2个：好用到哭、大数据、教科书般、小白必看、宝藏、绝绝子、神器、都给我冲、划重点、笑不活了、YYDS、秘方、我不允许、压箱底、建议收藏、停止摆烂、上天在提醒你、挑战全网、手把手、揭秘、普通女生、沉浸式、有手就能做、吹爆、好用哭了、搞钱必看、狠狠搞钱、打工人、吐血整理、家人们、隐藏、高级感、治愈、破防了、万万没想到、爆款、永远可以相信、被夸爆、手残党必备、正确姿势 
                4. 小红书平台的标题特性 
                4.1 控制字数在20字以内，文本尽量简短 
                4.2 以口语化的表达方式，拉近与读者的距离 
              二、正文创作技巧 
                1. 写作风格 
                    从列表中选出1个：严肃、幽默、愉快、激动、沉思、温馨、崇敬、轻松、热情、安慰、喜悦、欢乐、平和、肯定、质疑、鼓励、建议、真诚、亲切
                2. 写作开篇方法 
                    从列表中选出1个：引用名人名言、提出疑问、言简意赅、使用数据、列举事例、描述场景、用对比


             脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
             ```{wikipedia_search}```""")
        ]
    )

    model = ChatOpenAI(openai_api_key=api_key, temperature=creativity)

    title_chain = title_template | model
    script_chain = script_template | model

    title = title_chain.invoke({"subject": subject}).content

    search = WikipediaAPIWrapper(lang="zh")
    search_result = search.run(subject)

    script = script_chain.invoke({"title": title, "duration": video_length,
                                  "wikipedia_search": search_result}).content

    return search_result, title, script

# print(generate_script("sora模型", 1, 0.7, os.getenv("OPENAI_API_KEY")))