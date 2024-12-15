from zhipuai import ZhipuAI
from config import API_KEY

class ChatAPI:
    def __init__(self):
        # 初始化API客户端
        self.client = ZhipuAI(api_key=API_KEY)
        self.model = "glm-4"  # 使用GLM-4模型
        
    def send_message(self, message, history=None):
        """
        发送消息到AI并获取响应
        :param message: 用户输入的消息
        :param history: 对话历史记录
        :return: AI的响应
        """
        try:
            print("开始调用API...")
            print("使用的API密钥:", self.client.api_key)  # 检查API密钥
            print("发送的消息:", message)
            print("历史记录:", history)
            
            # 构建消息列表
            messages = []
            
            # 添加系统提示消息
            messages.append({
                "role": "system",
                "content": "你是一个友好的AI助手，能够提供专业、准确的回答。"
            })
            
            # 添加历史对话记录
            if history:
                messages.extend(history)
            
            # 添加用户当前消息
            messages.append({
                "role": "user",
                "content": message
            })
            
            print("完整的消息列表:", messages)
            
            # 调用API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                top_p=0.95,
                max_tokens=1024,
                stream=False
            )
            
            print("API原始响应:", response)
            
            # 获取AI响应
            ai_message = response.choices[0].message.content
            
            return {
                "success": True,
                "message": ai_message,
                "usage": response.usage
            }
            
        except Exception as e:
            print("API调用异常:", str(e))
            import traceback
            print("异常详情:", traceback.format_exc())
            return {
                "success": False,
                "error": str(e)
            }
    
    def stream_message(self, message, history=None):
        """
        使用流式输出发送消息
        :param message: 用户输入的消息
        :param history: 对话历史记录
        :yield: AI的响应片段
        """
        try:
            # 构建消息列表
            messages = []
            
            # 添加系统提示消息
            messages.append({
                "role": "system",
                "content": "你是一个友好的AI助手，能够提供专业、准确的回答。"
            })
            
            # 添加历史对话记录
            if history:
                messages.extend(history)
            
            # 添加用户当前消息
            messages.append({
                "role": "user",
                "content": message
            })
            
            # 调用API获取流式响应
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                top_p=0.95,
                max_tokens=1024,
                stream=True  # 启用流式输出
            )
            
            # 逐块返回响应
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"Error: {str(e)}" 