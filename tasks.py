import asyncio
import os

from invoke import task
from pyppeteer import launch

from shiori_generator import ShioriGenerator

@task
def gen_web(ctx):
    sg = ShioriGenerator(
        'data/timetable.csv',
        'data/room.csv',
        'data/sponsor.json',
    )
    sg.generate_web('templates/web/template.html', 'web/index.html')

@task
def gen_paper(ctx):
    sg = ShioriGenerator(
        'data/timetable.csv',
        'data/room.csv',
        'data/sponsor.json',
    )
    sg.generate_paper('templates/paper/template.html', 'paper/index.html')

# c.f. https://github.com/miyakogi/pyppeteer#usage
async def print_page(html_path, pdf_path):
    shiori_path = 'file://' + os.path.join(os.getcwd(), html_path)
    browser = await launch()
    page = await browser.newPage()

    # networkidle0 オプションを付けないとgfontsロード途中で
    # PDF化してしまうため、真っ白なPDFが生成される
    await page.goto(shiori_path, { 'waitUntil': 'networkidle0' })

    await page.pdf({'path': pdf_path })
    await browser.close()

@task
def gen_web_pdf(c):
    asyncio.get_event_loop().run_until_complete(print_page('./web/index.html', 'web-shiori.pdf'))

@task
def gen_paper_pdf(c):
    asyncio.get_event_loop().run_until_complete(print_page('./paper/index.html', 'paper-shiori.pdf'))
