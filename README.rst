#################
COVID19 DATA 処理
#################

******
/Tokyo
******


"東京都の感染者状況(個票)からテキストを抽出する (PDF=> CSV)

::

    pdf2tky.py   pdfplumber を使って PDF からテキスト情報を抽出する。
    cmp_year.py  year を補って、YMD 形式のリリース/発症/確定日を追加する。

データソース

::

    東京都福祉保健局 / 新型コロナウイルス感染症の都内感染者の状況 (PDF: 月曜更新)
    https://www.fukushihoken.metro.tokyo.lg.jp/iryo/kansen/todokedehcyouseisya.html
    (注:東京都の資料では、記号の丸[○]ではなく漢数字の零[〇]が使用されることがある。)


使い方
""""""

東京都の web から 0104.pdf をダウンロードして、./data フォルダーに保存した場合:

::

    # 以下のコマンドで data/0104.csv が出来る
    pdf2tky.py data/0104.pdf
    
    # 以下のコマンドで data/0104_c.csv (ファイル名に _c 付加)が出来る
    cmp_year.py data/0104.csv


BUGS
""""

::

    pdfplumber は、短い表を見落とす場合がある(例えば、相模原市 2021/01/08 最終ページ)。
    パラメーターの指定で調整できそうではあるが、良く分からない。
    最終レコードを目視で確認した方が良い。


