from flask import Flask, request, jsonify
from flask_cors import CORS
from chat_api import ChatAPI
import json
import traceback

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # 允许所有来源访问API

# 初始化ChatAPI
chat = ChatAPI()

@app.route('/api/chat', methods=['POST'])
def handle_chat():
    try:
        data = request.json
        messages = data.get('messages', [])
        
        print("收到的消息:", messages)  # 查看接收到的消息
        print("请求数据:", data)  # 打印完整的请求数据
        
        # 调用ChatAPI发送消息
        response = chat.send_message(
            message=messages[-1]['content'],  # 获取最新的用户消息
            history=messages[1:-1]  # 排除系统消息和最新消息
        )
        
        print("API响应:", response)  # 查看API响应
        
        if response['success']:
            return jsonify({
                'choices': [{
                    'message': {
                        'content': response['message']
                    }
                }]
            })
        else:
            print("API错误:", response.get('error'))
            print("错误详情:", traceback.format_exc())
            return jsonify({
                'error': response['error']
            }), 500
            
    except Exception as e:
        print("发生异常:", str(e))
        print("异常详情:", traceback.format_exc())
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 