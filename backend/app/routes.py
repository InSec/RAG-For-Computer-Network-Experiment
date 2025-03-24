from flask import Blueprint, request, jsonify
import openai


main_routes = Blueprint('main', __name__)


# 登录验证接口
@main_routes.route('/login', methods=['POST', 'GET'])
def login():
    data = request.json
    if data['username'] == 'admin' and data['password'] == '123456':
        return jsonify({'message': 'Login successful', 'status': 'success'})
    return jsonify({'message': 'Invalid credentials', 'status': 'error'})

# 智能问答接口
@main_routes.route('/qa', methods=['POST'])
def question_answering():
    question = request.json.get('question')
    context = "计算机网络实验相关知识"
    answer = f"根据你的问题'{question}'，回答是基于上下文：{context}"
    return jsonify({'answer': answer})
