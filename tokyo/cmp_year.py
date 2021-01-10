"""年を補完した日付を付加する。(for 東京都福祉保健局/都内感染者の状況)

東京都の資料には日付の項目に年の情報がないので、それを補完する。
各レコードの終端に、 Y/M/D 形式のリリース日、発症日、確定日を追加する。

使い方
------
data/0104.csv から data/0104_c.csv (ファイル名に _c 追加、Y/M/D タイムスタンプ追加)を作る場合:
$ cmp_year.py data/0104.csv

レコード構成
------------
 0:'リリース日'
 1:'居住地'
 2:'年代'
 3:'性別'
 4:'属性(職業等)'
 5:'渡航歴'
 6:'接触歴'
 7:'発症日'
 8:'確定日'
 9: '重症',
10 '退院等'
--- 以下を追加 ---
11:'リリース日YMD'
12:'発症日YMD'
13:'確定日YMD'

NOTES
-----
リリース日は昇順に並んでいることを仮定している。
再発で表が更新されたときに、各日付がどのように変更されるか分からないので、
正しい対処というのも分からない。

"""
import sys
import os
import re
from datetime import datetime, timedelta
import csv

def get_month_day(x):
    m = re.match(r'(\d+)月(\d+)日', x)
    if m:
        month = int(m.group(1))
        day = int(m.group(2))
    else:
        month = 0
        day = 0
    return month, day
    
def date_str(x):
    return x.strftime('%Y/%m/%d')
    
def complement_year(date_ref, m, d):
    """ 年を補完して日付を作る
    
    年が不明の月日をのうち基準日に近いものを選ぶ。
    探す範囲は、基準日の年を Y として Y±1 年。
    
    Parameters
    ----------
    date_ref, datetime : 規準日
    m, int : 月
    d, int : 日
    
    Returns
    -------
    date, datetime : 年を補完した日付
    
    Notes
    -----
    基準日として公表日を選ぶと、発症や診断は必ず過去になるので仕様は緩め。
    再発のケースの扱いなど不明な点も多いので、とりあえず差が小さいものを
    選ぶことにした。年の ambiguity を解決する方法として、基準日の月と目的
    の月の大小関係で場合分けすることが多いと思うが、ここでは、候補をいく
    つか計算したうえで、一番近いものを選んでいる。仕様との意味的な対応も
    よく、if の条件式の設定で悩む事もない。加えて、(見やすさはともかくと
    して、)その気になれば一つの式で表現できるという素敵な性質を有している。
    """
    yy = [date_ref.year + a for a in (-1, 0, 1)] # 年の候補
    dd = [datetime(a, m, d) for a in yy] # 対応する日付
    err_date = [(abs((a - date_ref).days), a) for a in dd] # 基準日からの差と日付
    err_, date = sorted(err_date)[0] # 昇順に並べた先頭(差が最小)
    if abs((date - date_ref).days) > 150:
        sys.stderr.write('WARNING : date %s - date_ref %s > 150 day \n' % (date, date_ref))
    return date
    
def _ymd(date_rel, x):
    """ ○月×日 ==> YYYY/MM/DD (YYYY は、date_rel 使って補完)
    
    Parameters
    ----------
    date_rel, datetime : リリース日
    x, str: 日付 '○月×日'
    
    Returns
    -------
    ym, str : 年月日を表す文字列 'YYYY/MM/DD'
    
    """
    m, d = get_month_day(x)
    if m != 0:
        date = complement_year(date_rel, m, d)
        ymd = date_str(date)
    else:
        ymd = ''
    return ymd
    
def main():
    """  *.csv と同じフォルダに *_c.csv を作る。
    
    ファイル名に _c を付加。
    各レコードの終端に、Y/M/D 形式の日付情報を追加。
    
    """
    path_src = sys.argv[1]
    with open(path_src, encoding='sjis') as csv_source:
        buf = [a for a in csv.reader(csv_source)]
    buf[0] = buf[0] + ['リリース日YMD', '発症日YMD', '確定日YMD'] # ヘッダー追加
    
    y_rel = 2020 # 年の初期値
    m_prv = None # 前のレコードの月
    for x in buf[1:]:  # skip header
        # リリース日(新年検出)
        #
        m_rel, d_rel = get_month_day(x[0]) # リリース日の月,日
        if m_prv and (m_rel < m_prv):
            y_rel = y_rel + 1
            print('detect new year %d %d %d ' % (y_rel, m_rel, d_rel))
        m_prv = m_rel
        date_rel = datetime(y_rel, m_rel, d_rel)
        
        # 追加情報
        x.append(date_str(date_rel))   # x[11] リリース日YMD
        x.append(_ymd(date_rel, x[7])) # x[12] 発症日YMD
        x.append(_ymd(date_rel, x[8])) # x[13] 確定日YMD
        
    fn_dir, fn_fn = os.path.split(path_src)
    fn_base, fn_ext = os.path.splitext(fn_fn)
    path_dst = os.path.join(fn_dir, '%s_c.csv' % (fn_base))
    with open(path_dst, 'w', newline='', encoding='sjis') as csv_file:
        wr = csv.writer(csv_file)
        wr.writerows(buf)
    
if __name__ == '__main__':
    main()
    
