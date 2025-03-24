from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

with open('data/class_info.json', 'r', encoding='utf-8') as f:
    class_data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message').strip()
    weekday = ['월요일', '화요일', '수요일', '목요일', '금요일']
    today_weekday = weekday[datetime.today().weekday()]

    if '시간표' in user_input:
        subjects = class_data["시간표"].get(today_weekday, [])
        text = f"[{today_weekday} 시간표]\n" + '\n'.join([f"{i+1}교시: {subj}" for i, subj in enumerate(subjects)])
        return jsonify({'reply': text, 'image': '/static/timetable.png'})

    if '학사일정' in user_input:
        return jsonify({
            'reply': '2025학년도 학사일정입니다. (1학기 & 2학기)',
            'image': ['/static/calendar_1.png', '/static/calendar_2.png']
        })

    if '선생님' in user_input and ('어디' in user_input or '교무실' in user_input or '계신' in user_input):
        return jsonify({'reply': class_data.get('선생님위치', '정보가 없습니다.')})

    return jsonify({'reply': "없는 정보입니다. 유도현에게 직접 물어봐주세요."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
