from chat_api import ChatAPI

def main():
    # 创建ChatAPI实例
    chat = ChatAPI()
    
    # 保存对话历史
    history = []
    
    print("欢迎使用AI聊天助手！输入 'quit' 退出对话。")
    
    while True:
        # 获取用户输入
        user_input = input("\n你: ")
        
        # 检查是否退出
        if user_input.lower() == 'quit':
            break
        
        # 发送消息并获取响应
        response = chat.send_message(user_input, history)
        
        if response["success"]:
            # 打印AI回复
            print("\nAI:", response["message"])
            
            # 保存对话历史
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": response["message"]})
        else:
            print("\n错误:", response["error"])

if __name__ == "__main__":
    main() 