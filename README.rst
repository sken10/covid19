*****************
COVID19 DATA ����
*****************

/Tokyo
======

"�����s�̊����ҏ�(�[)����e�L�X�g�𒊏o���� (PDF=> CSV)

::

    pdf2tky.py   pdfplumber ���g���� PDF ����e�L�X�g���𒊏o����B
    cmp_year.py  year �����āAYMD �`���̃����[�X/����/�m�����ǉ�����B

�f�[�^�\�[�X

::

    �����s�����ی��� / �V�^�R���i�E�C���X�����ǂ̓s�������҂̏� (PDF: ���j�X�V)
    https://www.fukushihoken.metro.tokyo.lg.jp/iryo/kansen/todokedehcyouseisya.html
    (��:�����s�̎����ł́A�L���̊�[��]�ł͂Ȃ��������̗�[�Z]���g�p����邱�Ƃ�����B)


�g����
------

�����s�� web ���� 0104.pdf ���_�E�����[�h���āA./data �t�H���_�[�ɕۑ������ꍇ:

::

    # �ȉ��̃R�}���h�� data/0104.csv ���o����
    pdf2tky.py data/0104.pdf
    
    # �ȉ��̃R�}���h�� data/0104_c.csv (�t�@�C������ _c �t��)���o����
    cmp_year.py data/0104.csv


BUGS
----

::

    pdfplumber �́A�Z���\�������Ƃ��ꍇ������(�Ⴆ�΁A���͌��s 2021/01/08 �ŏI�y�[�W)�B
    �p�����[�^�[�̎w��Œ����ł������ł͂��邪�A�ǂ�������Ȃ��B
    �ŏI���R�[�h��ڎ��Ŋm�F���������ǂ��B


