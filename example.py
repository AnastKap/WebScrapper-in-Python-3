import webscrapper

def main():
    document = webscrapper.WebScrap("example.html")

    #prints inner HTML of head element
    head = document.get_elements_by_tag_name("head")[0]
    print(head.get_innerHTML())

    #prints attributes of element with id = "hello"
    hello = document.get_element_by_id("hello")
    attrs = hello.get_attributes()
    for i in range(0, len(attrs)):
        print(attrs[i][0], "=", attrs[i][1], end = " | ")

main()
