import json
from datetime import datetime

# flack modules
from flask import Flask, render_template, redirect, Markup, escape

application = Flask(__name__)

DATA_FILE = 'norilog.json'


def save_data(start, finish, memo, created_at):
    """ 記録データを保存する
    :param start:   乗車駅
    :type  start:   str
    :param finish:  降車駅
    :type  finish:  str
    :param memo:    メモ
    :type  memo:    str
    :param created_at: 日付
    :type created_at: datetime.datetime
    :return: None
    """
    try:
        # json モジュールでデータベースファイルを開く
        database = json.load(open(DATA_FILE, mode='r', encoding='utf-8'))
    except FileNotFoundError:
        database = []

    database.insert(0, {
        'start': start,
        'finish': finish,
        'memo': memo,
        'created_at': created_at.strftime('%Y-%m-%d %H:%M')
    })

    json.dump(database, open(DATA_FILE, mode='w', encoding='utf-8'), indent=4, ensure_ascii=False)


def load_data():
    """ 記録データを return する """
    try:
        # json モジュールでデータベースファイルを開く
        database = json.load(open(DATA_FILE, mode='r', encoding='utf-8'))
    except FileNotFoundError:
        database = []

    return database


@application.template_filter('nl2br')
def nl2br_filter(s):
    """ 改行文字を br タグに変換するテンプレートフィルタ """
    return escape(s).replace('\n', Markup('<br>'))


@application.route('/')
def index():
    """ トップベージ
        テンプレートを使用してページを表示
    """
    # 記録データの読み込み
    rides = load_data()

    return render_template('index.html', rides=rides)


@application.route('/save', methods=['POST'])
def save():
    """ 記録用 URL """
    # 記録されたデータを取得
    start = request.form.get('start')  # 出発
    finish = request.form.get('finish')  # 到着
    memo = request.form.get('memo')  # メモ
    create_at = datetime.now()  # 記録日
    save_data(start, finish, memo, create_at)

    # 保存後、トップページにリダイレクト
    return redirect('/')


def main():
    application.run('127.0.0.1', 8000)


if __name__ == '__main__':
    # IPアドレス0.0.0.0の8000番ポートでアプリケーションを起動
    application.run('127.0.0.1', 8000, debug=True)
