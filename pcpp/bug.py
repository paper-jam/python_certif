





https://edube.org/learn/pcpp1-4-gui-programming/a-small-lexicon-of-widgets-part-3-22

line 9 : are_you_sure
line 34 :  AreYouSure


https://edube.org/learn/pcpp1-4-gui-programming/shaping-the-main-window-and-conversing-with-the-user-10
window = tk.Tk()


https://edube.org/learn/pcpp1-working-with-restful-apis/json-our-new-friend-8
property examples should contains quotes
{ 
"x": 123,
"y": -1
}

https://edube.org/learn/pcpp1-working-with-restful-apis/what-is-xml-and-why-do-we-prefer-to-use-json-14
 last line of code 
 print(' =', prop.text) is not correctly indented


cars_for_sale = xml.etree.ElementTree.parse('cars.xml').getroot()
print(cars_for_sale.tag)
for car in cars_for_sale.findall('car'):
    print('\t', car.tag)
    for prop in car:
        print('\t\t', prop.tag, end='')
        if prop.tag == 'price':
            print(prop.attrib, end='')
        print(' =', prop.text)


