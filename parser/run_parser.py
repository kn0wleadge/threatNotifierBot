import asyncio
import logging

from playwright.async_api import async_playwright, Playwright
import time

from tgbot.database.add_threat import add_threat
from tgbot.database.connect_soft import connect_soft

from tgbot.services.find_soft_in_description import find_soft_in_description
from tgbot.database.get_all_soft import get_all_soft
from tgbot.database.find_threatid_by_info import get_threatid

"""async def get_detail(context, url):
    page = await context.new_page()
    await page.goto(url,timeout = 0) 
    await page.wait_for_load_state(state="networkidle",timeout = 60000)
    await page.wait_for_timeout(0)
    page.close()

#async def open_new_pages(context, urls):
    # Creating tasks: https://docs.python.org/3.11/library/asyncio-task.html#creating-tasks
    background_tasks = set()
    for url in urls:
        task = asyncio.create_task(
            get_detail(context, url)
        )
        background_tasks.add(task)
    
    #Awaiting for each of the tasks:
    for t in background_tasks:
        await t
"""
async def fetch_specific_info(page, url):
    await page.goto(url,timeout = 0)
    data = {}
    data["url"] = url
    # Extracting "Описание уязвимости"
    description_row = await page.query_selector("//table[@class='table table-striped attr-view-table']//tr[td[contains(text(),'Описание уязвимости')]]")
    if description_row:
        description = await description_row.query_selector("td:nth-child(2)")
        description_text = await description.inner_text()
        data["Description"] = description_text

 
    # Extracting "Уровень опасности уязвимости"
    danger_level_row = await page.query_selector("//table[@class='table table-striped attr-view-table']//tr[td[contains(text(),'Уровень опасности уязвимости')]]")
    if danger_level_row:
        danger_level = await danger_level_row.query_selector("td:nth-child(2)")
        data["Danger level"] = await danger_level.inner_text()

    # Extracting "Возможные меры по устранению уязвимости"
    mitigation_measures_row = await page.query_selector("//table[@class='table table-striped attr-view-table']//tr[td[contains(text(),'Возможные меры по устранению уязвимости')]]")
    if mitigation_measures_row:
        mitigation_measures = await mitigation_measures_row.query_selector("td:nth-child(2)")
        rec_solve = await mitigation_measures.inner_text()
        if rec_solve.find(' раскрыть\n') != -1:
            rec_solve = rec_solve[10:]
        data["Solving method"] = rec_solve
    threat_id = await get_threatid(data)
    if (threat_id):
        print('\n ---threat already exists--')
        data = []
    else:    
        soft_names = await get_all_soft()
        if len(await find_soft_in_description(description=description_text, soft_names=soft_names)) == 0:
            data = []
            print('---no needed soft---')
            print('---useless threat---')

    return data

async def run(playwright: Playwright) -> list:
    start_time = time.time()
    chromium = playwright.chromium
    browser = await chromium.launch(headless=True)
    context = await browser.new_context(ignore_https_errors=True);
    page1 = await context.new_page()
    page2 = await context.new_page()
    page3 = await context.new_page()
    page4= await context.new_page()
    page5 = await context.new_page()
    page6 = await context.new_page()
    pages = [page1,page2,page3,page4,page5,page6]
    mainpage = await context.new_page()
    await mainpage.goto('https://bdu.fstec.ru/vul?sort=datv&size=10', timeout = 0)
    links =  await mainpage.query_selector_all("a.confirm-vul")

    #Части ссылок на подробные описания угроз
    url_parts = []

    #Добавление в url_parts всех частей ссылок
    for link in links:
            text = await link.inner_text()
            href = await link.get_attribute("href")
            print(f"Текст: {text}, Ссылка: {href}")
            url_parts.append(href)
    #mainpage.close()
    urls = []
    #Создание полных ссылок для всех запаршенных угроз
    for url_part in url_parts:
        url = 'https://bdu.fstec.ru'
        url = url + url_part
        urls.append(url)

    #urls = urls[0]

    #print(f'urls - {urls}')
    all_url_checked:bool = False
    all_data = []
    url_counter = 1
    #Цикл будет работать до тех пор, пока не будут запаршены угрозы по всем ссылкам
    while not all_url_checked:
        
        if (len(urls) < 6):
            some_urls = urls[:len(urls)]
        else:
            some_urls = urls[:6]

        for i in range(0,len(some_urls),1):
            print('------------------------')
            print(f'threat №{url_counter}')
            print('------------------------')
            url_counter = url_counter + 1
            try:
                data = await fetch_specific_info(pages[i], some_urls[i])
                print(f'fetched threat data - {data}')

                #Если данные валидны - добавляем их в список на добавление
                if (len(data) > 0):
                    all_data.append(data)
            except Exception as e:
                print(f'Ошибка при парсинге - {e}')


        if (len(urls) < 6):
            all_url_checked = True
        else:
            urls = urls[6:]

    await browser.close()
    print("--- %s seconds ---" % (time.time() - start_time))
    return all_data

async def main():
    async with async_playwright() as playwright:
        #Парсинг данных об угрозах с сайта
        parsed_data = await run(playwright)

        for threat in parsed_data:

            #Добавление угрозы в БД
            await add_threat(threat)
            #Добавление связи БД с софтом
            await connect_soft(threat['url'])

    return parsed_data
