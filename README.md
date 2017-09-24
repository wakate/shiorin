# shiorin

イベントのしおりをHTMLで生成するツールです。
[情報科学若手の会](wakate.org)で使用します。

## shiorinについて

### ディレクトリ構成
```
.
├── README.md
├── abst_table.py
├── common.css
├── data
│   ├── room.csv
│   └── timetable.csv
├── index.html
├── info
│   ├── 01_wifi.md
│   ├── 02_twitter.md
│   ├── 03_access.md
│   ├── 04_contact_for_yamaki.md
│   └── 05_contact_for_kanji.md
├── page_generator.py
├── room.py
├── table.css
├── table.py
├── tasks.py
├── template.html
├── text.css
└── time_table.py
```

## Installation

### 用意するもの

- 実行環境
    - [python 3.6.1](https://www.python.org/downloads/)
    - [pip 9.0.1](https://pip.pypa.io/en/stable/installing/)

- 足りないファイル
    - `template.html`
    - `data/timetable.csv`
    - `data/room.csv`
    - `info/***.md`

### インストール手順

```
git clone https://github.com/hnmx4/shiorin.git
cd shiorin
pip install invoke Jinja2 Markdown
mv ***/template.html ./
mv ***/data ./
mv ***/info ./
```

## 使い方

```
invoke gen_web
```
