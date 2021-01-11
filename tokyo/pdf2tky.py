"""東京都の感染者状況からテキストを抽出 (PDF=> CSV) / pdfplumber 版

使い方
------
data/0104.pdf から data/0104.csv を作る場合:
$ pdf2tky.py data/0104.pdf

データソース
東京都福祉保健局 / 新型コロナウイルス感染症の都内感染者の状況 (PDF: 月曜更新)
https://www.fukushihoken.metro.tokyo.lg.jp/iryo/kansen/todokedehcyouseisya.html

NOTES
-----
PDF の表抽出には camelot を使っていましたが、pdfplumber に変えることで 20倍速く
なりました。表の形が単純なら、pdfplumber が良さそうです。
1ページに表が 1 つだけであることを仮定しています (extract_tables ではなく
extract_table を使用)

"""
import sys
import os
import re
import unicodedata
import csv

import pdfplumber

def _c(x):
    """正規化と空白削除
    """
    y = re.sub(r'\s', r'', x) # 空白削除
    z = unicodedata.normalize('NFKC', y) # 正規化
    return z
    
def one_table(table, n_page):
    """テーブルの中味の確認とヘッダー行の切り分け
    
    Notes
    -----
    n_page == 1 の分岐は、一つ上の階層で処理した方が良いが、
    データの書式情報が分散するのを嫌ってこのまま。
    
    """
    # 正規化
    lines = [[_c(a) for a in b] for b in table]
    
    buf = []
    for (n_rec, line) in enumerate(lines):
        if re.match(r'リリース日', line[0]):
            # ヘッダーを出力は、先頭ページのみ
            if n_page == 1:
                buf.append(line)
        elif re.match(r'\d+月\d+日', line[0]):
            buf.append(line)
        else:
            sys.stderr.write('PANIC page %d rec %d : %s\n' % (n_page, n_rec, line))
    return buf
    
def read_pdf(path_pdf):
    """ PDF の表から、text 情報を抽出して 2 次元のリストを作る
    
    """
    buf = []
    with pdfplumber.open(path_pdf) as pdf:
        for (n, page) in enumerate(pdf.pages, start=1):
            sys.stderr.write('page %d/%d\r' % (n, len(pdf.pages)))
            table = page.extract_table()
            buf = buf + one_table(table, n)
    return buf
    
def change_ext(path_src, ext_dst):
    """ path_src の拡張子を ext_dst に変更する。
    ext_dst の先頭は '.' を想定。
    
    """
    assert(ext_dst[0] == '.')
    fn_dir, fn_fn = os.path.split(path_src)
    fn_base, fn_ext = os.path.splitext(fn_fn)
    path_dst = os.path.join(fn_dir, '%s%s' % (fn_base, ext_dst))
    return path_dst
    
def main():
    """  *.pdf と同じフォルダに *.csv を作る
    """
    path_pdf = sys.argv[1]
    buf = read_pdf(path_pdf)
    path_csv = change_ext(path_pdf, '.csv')
    with open(path_csv, 'w', newline='', encoding='sjis') as csv_file:
        csv.writer(csv_file).writerows(buf)
    
if __name__ == '__main__':
    main()
    
