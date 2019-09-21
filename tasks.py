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
    templates_dir = os.path.join('templates', 'paper')
    templates = {
        'cover': os.path.join(templates_dir, 'cover.html'),
        'timetable': os.path.join(templates_dir, 'timetable.html'),
        'room': os.path.join(templates_dir, 'room.html'),
        'ryokan': os.path.join(templates_dir, 'ryokan.html'),
        'info': os.path.join(templates_dir, 'info.html')
    }
    sg.generate_paper(templates, 'paper')

# c.f. https://github.com/miyakogi/pyppeteer#usage
async def print_page():
    shiori_path = 'file://' + os.path.join(os.getcwd(), './web/index.html')
    browser = await launch()
    page = await browser.newPage()

    # networkidle0 オプションを付けないとgfontsロード途中で
    # PDF化してしまうため、真っ白なPDFが生成される
    await page.goto(shiori_path, { 'waitUntil': 'networkidle0' })

    await page.pdf({'path': 'shiori.pdf'})
    await browser.close()

@task
def gen_pdf(c):
    asyncio.get_event_loop().run_until_complete(print_page())
