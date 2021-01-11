########################
COVID19 自治体データ収集
########################

/Tokyo
======

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

::

    東京都の web から 0104.pdf をダウンロードして、./data フォルダーに保存した場合:
    
    # 以下のコマンドで data/0104.csv が出来る
    pdf2tky.py data/0104.pdf
    
    # 以下のコマンドで data/0104_c.csv (ファイル名に _c 付加)が出来る
    cmp_year.py data/0104.csv


NOTES

::

    東京都の資料は 1ページに表が 1 つだけなので、.extract_table() で大丈夫ですが、
    1ページに表が複数存在する資料を扱う場合は、.extract_tables() に変更する必要があります。


Links

    `新型コロナウイルス感染症に関する相模原市発表資料（発生状況等）のPDFをCSVに変換
    <https://qiita.com/barobaro/items/55ad358ad7ef4a07c65f>`_

