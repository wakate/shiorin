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
│   ├── room.csv
│   ├── sponsor.json
│   └── timetable.csv
├── md
│   ├── info
│   │   └── 0X_***.md
│   └── ryokan
│       └── 0X_***.md
├── page_generator.py
├── room.py
├── table.py
├── tasks.py
├── time_table.py
├── web
│   ├── css
│   │   ├── common.css
│   │   ├── header.css
│   │   ├── table.css
│   │   └── text.css
│   ├── image
│   │   └── ***.png
│   ├── index.html
│   └── logo
│       └── ***.png
└── web_template.html
```

## Installation

### 用意するもの

- 実行環境
    - [python 3.6.1](https://www.python.org/downloads/)
    - [pip 9.0.1](https://pip.pypa.io/en/stable/installing/)

- 足りないファイル/ディレクトリ
    - `data/`
    - `md/info/`
    - `md/ryokan/`
    - `web/image/`
    - `web/logo/`

### インストール手順

```
git clone https://github.com/hnmx4/shiorin.git
cd shiorin
pip install invoke Jinja2 Markdown
mv ***/data ./
mv ***/md ./
mv ***/web/image ./web/
mv ***/web/logo ./web/
```

## 使い方

```
invoke gen_web
```
