from bs4 import BeautifulSoup #importer beauiful soup 

with open(r'C:\Users\kitco\Desktop\Portfolio\Beautiful Soup 4\Scarping Basics\index.html', 'r') as html_file: # opens index.html file with read perms and saves it as html_file variable
    content = html_file.read() #read method reading html file content

    soup = BeautifulSoup(content, 'lxml')
    course_cards = soup.find_all('div', class_='card')
    for course in course_cards:
        course_name = course.h5.text
        course_price = course.a.text.split()[-1]
        print(f'{course_name} costs {course_price}')