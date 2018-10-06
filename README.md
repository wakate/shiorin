# shiorin

イベントのしおりをHTMLで生成するツールです。
[情報科学若手の会](wakate.org)で使用します。

## shiorinについて

### ディレクトリ構成
```
.
├── README.md
├── abst_table.py
├── data
├── md
├── paper
├── room.py
├── shiori_generator.py
├── table.py
├── tasks.py
├── templates
├── time_table.py
└── web
```

## Installation

### 用意するもの

- 実行環境
    - [python 3.6.1](https://www.python.org/downloads/)
    - [pip 9.0.1](https://pip.pypa.io/en/stable/installing/)

- 足りないディレクトリ

  次のディレクトリとファイルを入手して、適切に配置してください。
    - `data`
    - `md`
    - `web/image`
    - `web/logo`
    - `paper/image`
    - `paper/logo`

### インストール手順

```
git clone https://github.com/hnmx4/shiorin.git
cd shiorin
pip install invoke Jinja2 Markdown
mv ***/data ./
mv ***/md ./
mv ***/web/image ./web/
mv ***/web/logo ./web/
mv ***/paper/image ./paper/
mv ***/paper/logo ./paper/
```

## 使い方

```
## generate web_shiori
invoke gen-web
ls web
css        image      index.html logo

## generate paper_shiori
invoke gen-paper
ls paper
cover.html     css            image          info.html      logo           room.html      ryokan.html    timetable.html
```
