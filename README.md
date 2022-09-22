# shiorin

イベントのしおりをHTMLで生成するツールです。
[情報科学若手の会](wakate.org)で使用します。

## shiorinについて

### ディレクトリ構成
```
.
├── README.md
├── abst_table.py
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
    - [poetry](https://python-poetry.org)
    - 日本語フォント(ex. fonts-ipafont-gothic fonts-ipafont-mincho)

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
git clone https://github.com/wakate/shiorin.git
cd shiorin
poetry install
poetry run pyppeteer-install
```

## 使い方

```
$ invoke gen-web # generate web_shiori
$ ls web
css        image      index.html logo
$ invoke gen-web-pdf # generate pdf from web_shiori
$ invoke gen-paper # generate paper_shiori
$ ls paper
cover.html     css            image          info.html      logo           room.html      ryokan.html    timetable.html
$ invoke gen-paper-pdf # generate pdf from paper_shiori
```
