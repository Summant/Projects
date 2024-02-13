from bs4 import BeautifulSoup
import requests as rq


def main():
    # Get user input of fighter names
    f_name = input("First Name: ")
    l_name = input("Last Name: ")
    search_char = l_name[0]
    fighter_attributes = {"Name": f"{f_name} {l_name}",
                          "Nickname": '',
                          "Height": '',
                          "Weight": '',
                          "Reach": '',
                          "Stance": '',
                          "W": '',
                          "L": '',
                          "D": '',
                          "Belt": ''}

    # setup link + html
    url = f'http://ufcstats.com/statistics/fighters?char={search_char}&page=all'
    result = rq.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    lst_of_attr = []
    index = -1

    # Parses html into list of names/stats
    find_stats_table = soup.find_all(class_='b-statistics__table-col')
    for tag in find_stats_table:
        if tag:
            lst_of_attr.append(tag.text.strip())

    # Finds location of fighter
    for i in range(len(lst_of_attr)-1):
        if lst_of_attr[i] == f_name and lst_of_attr[i+1] == l_name:
            index = i + 2

    # Assigns and Returns Information
    if index != -1:
        fighter_attributes["Nickname"] = lst_of_attr[index]
        fighter_attributes["Height"] = (lst_of_attr[index+1][0] + "ft."
                                        + lst_of_attr[index+1][2:-1:1] + "in.")
        fighter_attributes["Weight"] = lst_of_attr[index+2]
        fighter_attributes["Reach"] = lst_of_attr[index+3]
        fighter_attributes["Stance"] = lst_of_attr[index+4]
        fighter_attributes["W"] = lst_of_attr[index+5]
        fighter_attributes["L"] = lst_of_attr[index+6]
        fighter_attributes["D"] = lst_of_attr[index+7]
        fighter_attributes["Belt"] = lst_of_attr[index+8]
        for elem in list(fighter_attributes):
            print(f"{elem}: {fighter_attributes[elem]}")
    else:
        print("Fighter Not Found")


if __name__ == '__main__':
    main()
