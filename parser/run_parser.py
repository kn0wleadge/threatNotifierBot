import asyncio
import logging

from playwright.async_api import async_playwright, Playwright
import time

from tgbot.database.add_threat import add_threat
from tgbot.database.connect_soft import connect_soft
from tgbot.database.connect_user import connect_user

from tgbot.services.find_soft_in_description import find_soft_in_description
from tgbot.database.get_all_soft import get_all_soft
from tgbot.database.find_threatid_by_info import get_threatid

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
        matched_soft = await find_soft_in_description(description=description_text, soft_names=soft_names)
        if len(matched_soft) == 0:
            data = []
            print('---no needed soft---')
            print('---useless threat---')
        else:
            data["Soft"] = matched_soft

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
        #parsed_data = [{'url': 'https://bdu.fstec.ru/vul/2024-04914', 'Description': 'Уязвимость сервера средства криптографической защиты OpenSSH связана с повторным использованием ранее освобожденной памяти из-за конкурентного доступа к ресурсу (состояние гонки). Эксплуатация уязвимости может позволить нарушителю, действующему удалённо, выполнить произвольный код с root-привилегиями', 'Danger level': 'Высокий уровень опасности (базовая оценка CVSS 2.0 составляет 7,6)\nКритический уровень опасности (базовая оценка CVSS 3.0 составляет 9)', 'Solving method': 'Установка обновлений из доверенных источников.\nВ связи со сложившейся обстановкой и введенными санкциями против Российской Федерации рекомендуется устанавливать обновления программного обеспечения только после оценки всех сопутствующих рисков.\n\nКомпенсирующие меры:\n- для ограничения возможности эксплуатации в sshd_config выставить параметр «LoginGraceTime=0»;\n- установить для LoginGraceTime значение 0 в /etc/ssh/sshd_config и перезапустить sshd;\n- использование антивирусного программного обеспечения для отслеживания попыток эксплуатации уязвимости;\n- использование средств межсетевого экранирования для ограничения возможности удалённого доступа.\n\nИспользование рекомендаций производителя:\nДля FreeBSD:\nhttps://www.freebsd.org/security/advisories/FreeBSD-SA-24:04.openssh.asc\n\nДля OpenSSH:\nhttps://lists.mindrot.org/pipermail/openssh-unix-dev/2024-July/041430.html\n\nДля Debian GNU/Linux:\nhttps://security-tracker.debian.org/tracker/CVE-2024-6387', 'Soft': ['OpenSSH'], 'id': 79}, {'url': 'https://bdu.fstec.ru/vul/2024-04858', 'Description': 'Уязвимость программной платформы на базе git для совместной работы над кодом GitLab связана с недостатками разграничения доступа. Эксплуатация уязвимости может позволить нарушителю, действуюшему удалённо, выполнить произольный код путём запуска пайплайнов от имени других пользователей', 'Danger level': 'Высокий уровень опасности (базовая оценка CVSS 2.0 составляет 8,5)\nКритический уровень опасности (базовая оценка CVSS 3.0 составляет 9,6)', 'Solving method': 'Установка обновлений из доверенных источников.\nВ связи со сложившейся обстановкой и введенными санкциями против Российской Федерации рекомендуется устанавливать обновления программного обеспечения только после оценки всех сопутствующих рисков.\n\nКомпенсирующие меры:\n- минимизация пользовательских привилегий;\n- отключение/удаление неиспользуемых учётных записей пользователей;\n- использование средств межсетевого экранирования для ограничения возможности удалённого доступа;\n- использование виртуальных частных сетей для организации удаленного доступа (VPN).\n\nИспользование рекомендаций производителя:\nhttps://about.gitlab.com/releases/2024/06/26/patch-release-gitlab-17-1-1-released/', 'Soft': ['git', 'Git'], 'id': 80}, {'url': 'https://bdu.fstec.ru/vul/2024-04913', 'Description': 'Уязвимость компонента LibreOfficeKit пакета офисных программ LibreOffice связана с ошибками при проверке TLS-сертификата. Эксплуатация уязвимости может позволить нарушителю, действуюшему удалённо, выполнить произольный код', 'Danger level': 'Критический уровень опасности (базовая оценка CVSS 2.0 составляет 10)\nКритический уровень опасности (базовая оценка CVSS 3.0 составляет 9,8)', 'Solving method': 'Установка обновлений из доверенных источников.\nВ связи со сложившейся обстановкой и введенными санкциями против Российской Федерации рекомендуется устанавливать обновления программного обеспечения только после оценки всех сопутствующих рисков.\n\nКомпенсирующие меры:\n- использование SIEM-систем для отслеживания попыток эксплуатации уязвимости;\n- использование антивирусного программного обеспечения для открытия файлов, полученных из недоверенных источников;\n- использование средств межсетевого экранирования для ограничения возможности удалённого доступа.\n\nИспользование рекомендаций производителя:\nhttps://www.libreoffice.org/about-us/security/advisories/cve-2024-5261', 'Soft': ['LibreOffice'], 'id': 81}]
        print('data parsed')
        added_threats = []
        for threat in parsed_data:

            #Добавление угрозы в БД
            threat_added:bool = await add_threat(threat)

            if threat_added:
                #Добавление связи угрозы с софтом в БД
                await connect_soft(threat['url'])

                #Добавления связи угрозы с пользователем в БД
                threat_with_id = await connect_user(threat)
                added_threats.append(threat_with_id)

                
    return added_threats
