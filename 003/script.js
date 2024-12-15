// 添加到现有的script.js文件顶部
// 处理导航栏滚动效果
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// 处理导航链接点击事件
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        if (link.classList.contains('modal-trigger')) {
            e.preventDefault();
            // 这里可以添加显示AI对话框的逻辑
        }
    });
});

// 初始化Swiper轮播图
const swiper = new Swiper('.swiper', {
    loop: true,
    pagination: {
        el: '.swiper-pagination',
    },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    autoplay: {
        delay: 3000,
    },
});

// 聊天相关的DOM元素
const chatHistory = document.getElementById('chatHistory');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const clearButton = document.getElementById('clearButton');
const aiTyping = document.querySelector('.ai-typing');

// 保存对话历史
let messageHistory = [];

// 创建并添加消息到聊天界面
function addMessage(content, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = content;
    
    const messageTime = document.createElement('div');
    messageTime.className = 'message-time';
    messageTime.textContent = new Date().toLocaleTimeString();
    
    messageDiv.appendChild(messageContent);
    messageDiv.appendChild(messageTime);
    
    chatHistory.appendChild(messageDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

// 发送消息到API
async function sendToAI(message) {
    try {
        // 显示加载状态
        aiTyping.style.display = 'block';
        
        // 准备发送的消息
        const messages = [
            {
                "role": "system",
                "content": "你是一个友好的AI助手，能够提供专业、准确的回答。"
            },
            ...messageHistory,
            {
                "role": "user",
                "content": message
            }
        ];
        
        // 发送API请求
        const response = await axios.post('http://localhost:5000/api/chat', {
            model: "glm-4-plus",
            messages: messages,
            temperature: 0.7,
            top_p: 0.95,
            max_tokens: 1024
        });
        
        // 处理响应
        const aiResponse = response.data.choices[0].message.content;
        
        // 保存对话历史
        messageHistory.push(
            { "role": "user", "content": message },
            { "role": "assistant", "content": aiResponse }
        );
        
        // 显示AI回复
        addMessage(aiResponse, 'ai');
        
    } catch (error) {
        console.error('API调用错误:', error);
        addMessage('抱歉，发生了一些错误，请稍后重试。', 'ai');
    } finally {
        // 隐藏加载状态
        aiTyping.style.display = 'none';
    }
}

// 发送消息处理函数
async function handleSend() {
    const message = userInput.value.trim();
    if (!message) return;
    
    // 显示用户消息
    addMessage(message, 'user');
    userInput.value = '';
    
    // 发送到AI
    await sendToAI(message);
}

// 事件监听
sendButton.addEventListener('click', handleSend);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
    }
});

clearButton.addEventListener('click', () => {
    chatHistory.innerHTML = '';
    messageHistory = [];
    // 添加初始欢迎消息
    addMessage('你好！我是智谱AI助手，很高兴为您服务。让我们开始对话吧！', 'ai');
}); 