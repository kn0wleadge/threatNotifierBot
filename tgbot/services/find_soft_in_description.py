
async def find_soft_in_description(description:str, soft_names:list[str]) -> list[str]:
    print('searching for soft in description...')
    result = []
    low_description =description.lower() + ' '
    for name in soft_names:
        #Для поиска в середине описания
        format_name1 = name.lower()
        format_name1 = ' ' + format_name1 + ' '

        #Для поиска в конце описания
        format_name2 = name.lower()
        format_name2 = ' ' + format_name2

        #Для поиска в начале описания
        format_name3 = name.lower()
        format_name3 = name.lower() + ' '

        if low_description.find(format_name1) != -1  or low_description.find(format_name3) == 0:
            result.append(name)

    print(f"found soft - {result}")
    return result