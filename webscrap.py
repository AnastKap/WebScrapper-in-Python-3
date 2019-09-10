#TODO: cannot read tag attributes where there are spaces (Fixed)
#TODO: cannot undertand when < sign does not indicate element tag start...it's special characters issue
#TODO: cannot undrestand comments (Fixed)



#An empty element when no element found from element finding tecniques
class EmptyElement():
    def __init__(self):
        self.__elements = []  #child elements
        
        self.__tag = ""  #element tag

empty = EmptyElement


class WebScrap:
    def __init__(self, filename, enc = "utf-8"):
        file = open(filename, "r", encoding = enc)
        self.__doc = file.read()
        del file

        self.__index = 0
        self.__elements = []
        self.__innerHTML = self.__doc

        self.parse_elems()
        
    def parse_elems(self):
        while self.__index < (len(self.__doc) - 1):
            if (str(self.__doc[self.__index]) + str(self.__doc[self.__index + 1])) == "<!":
                self.__index += 2
            if self.__doc[self.__index] == "<":
                self.__elements.append(Element(self.__index, empty, self.__doc)) #Needs to be changed
                self.__index = self.__elements[len(self.__elements) - 1].get_element_end()
            else:
                self.__index += 1

    def get_element_by_id(self, id2find):
        for i in range(0, len(self.__elements)):
            ret_obj = self.__elements[i].get_element_by_id(id2find) #Returned Object
            if ret_obj != empty:
                return ret_obj

        #If above fails
        return empty

    def get_elements_by_tag_name(self, tag):
        found_elems_list = []
        for i in range(0, len(self.__elements)):
            ret_list = self.__elements[i].get_elements_by_tag_name(tag)
            for j in range(0, len(ret_list)):
                found_elems_list.append(ret_list[j])

        return found_elems_list

    def get_elements(self):
        return self.__elements

    def get_innerHTML(self):
        return self.__innerHTML

    def print_tags(self, tab = 0):
        for i in range(0, len(self.__elements)):
            for j in range(0, tab):
                print("\t", end = "")
            print(self.__elements[i].get_tag())
            if len(self.__elements[i].get_elements()) != 0:
                self.__elements[i].print_tags(tab + 1)

    def print_attributes(self, tab = 0):
        for j in range(0, tab):
            print("\t", end = "")
        print("Document:")

        for i in range(0, len(self.__elements)):
            self.__elements[i].print_attributes(tab + 1)

    def print_elements_with_id(self, tab = 0):
        for j in range(0, tab):
            print("\t", end = "")
        print("Document:", self.__id)
        for i in range(0, len(self.__elements)):
            self.__elements[i].print_elements_with_id(tab + 1)



class Element:
    def __init__(self, start_index, parent, doc):
        self.__doc = doc
        
        self.__elements = []  #child elements
        self.__innerHTML = ""
        
        self.__tag = ""  #element tag
        self.__parent = parent #The parent node
        self.__attributes = []  #list of lists with two list elements
        
        self.__start_i = start_index  #where whole element starts
        self.__start_tag_name_end = 0
        self.__start_tag_end = 0
        self.__end_tag_start = 0  #where the end tag is located
        self.__end_tag_end = 0   #where the end tag ends
        self.__end = 0  #where whole element ends (after end tag)

        self.__id = ""  #The id of current element (if any)

        self.__is_empty_tag = False  #if it is a tag which start tag ends in />

        self.__tag, self.__start_tag_name_end = self.find_tag(self.__start_i + 1)

        self.__start_tag_end = self.find_attributes(self.__start_tag_name_end + 1)

        if self.__is_empty_tag == False:
            self.parse_inner_tags()
            self.parse_inner_html()
        else:
            self.__end = self.__start_tag_end
            #print("Empty Tag", self.__tag)

    def find_tag(self, from_index):
        index = from_index
        tag = ""
        while (self.__doc[index] != " ") and (self.__doc[index] != ">") and self.__doc[index] != "/":
            tag += self.__doc[index]
            index += 1
            if (index + 1) > len(self.__doc):
                break
        return tag, (index - 1)

    def find_attributes(self, from_index):
        index = from_index
        attribute = ""
        value = ""

        if (self.__doc[index] + self.__doc[index + 1]) == "/>":
            self.__is_empty_tag = True
            index += 1
        while self.__doc[index] != ">":
            #Find spaces
            while self.__doc[index] == " ":
                index += 1
            #Find attribute
            if (self.__doc[index] + self.__doc[index + 1]) == "/>":
                self.__is_empty_tag = True
                index += 1
                break
            while self.__doc[index] != " " and self.__doc[index] != "=":
                attribute += self.__doc[index]
                index += 1
            while self.__doc[index] == " ":
                index += 1
            #Check if it finds "=" character...otherwise it's an attribute without a value
            if self.__doc[index] == "=":
                index += 1
                #Find spaces
                while self.__doc[index] == " ":
                    index += 1
                #Check if value is in the form "..." or not (used in order to accept values with spaces in them)
                if self.__doc[index] == '"':
                    index += 1
                    while self.__doc[index] != '"':
                        value += self.__doc[index]
                        index += 1
                    index += 1
                else:
                    while self.__doc[index] != " " and self.__doc[index] != ">" and self.__doc[index] != "/":
                        value += self.__doc[index]
                        index += 1

            #Here it will be checked if attribute is one of those that we need to identify elements
            if attribute == "id" and self.__id == "":
                self.__id = value
            self.__attributes.append([attribute, value])
            attribute = ""
            value = ""

        return index
            

    def parse_inner_tags(self):
        index = self.__start_tag_end + 1
        while index < (len(self.__doc) - 1):
            #If it is a comment
            if (self.__doc[index] + self.__doc[index + 1] + self.__doc[index + 2] + self.__doc[index + 3]) == "<!--":
                while (self.__doc[index] + self.__doc[index + 1] + self.__doc[index + 2]) != "-->":
                    index += 1
            #If it is something like <!DOCTYPE html>
            elif (self.__doc[index] + self.__doc[index + 1]) == "<!":
                index += 2
            #If it meets the end of a tag
            elif (self.__doc[index] + self.__doc[index + 1]) == "</":
                end_tag, end_i = self.find_tag(index + 2)
                self.__end_tag_start = index
                self.__end_tag_end = end_i
                #Check if indeed end tag found equals current element's tag
                if end_tag == self.__tag:
                    self.__end = end_i
                    index = end_i + 1
                    break
                #This if the end_tag found is not equal to this element tag (in case where there is no end tag by accident)
                else:
                    print("bad form found", self.__tag)
                    self.__elements = [] #set elements list back to empty
                    self.__end = self.__start_tag_end
                    break
            #If it meets the start of a tag
            elif self.__doc[index] == "<":
                self.__elements.append(Element(index, self, self.__doc))
                index = self.__elements[len(self.__elements) - 1].get_element_end() + 1
            #Any other case
            else:
                index += 1

    def parse_inner_html(self):
        index = self.__start_tag_end + 1
        while index != self.__end_tag_start:
            self.__innerHTML += self.__doc[index]
            index += 1

    def get_element_end(self):
        return self.__end
        
    def get_tag(self):
        return self.__tag

    def get_parent(self):
        return self.__parent

    def get_elements(self):
        return self.__elements

    def get_attributes(self):
        return self.__attributes

    def get_attribute_value(self, attribute):
        for i in range(0, len(self.__attributes)):
            if self.__attributes[i][0] == attribute:
                return self.__attributes[i][1]
        raise Exception

    def get_innerHTML(self):
        return self.__innerHTML

    def get_element_by_id(self, id2find):
        if self.__id == id2find:
            return self
        else:
            for i in range(0, len(self.__elements)):
                ret_obj = self.__elements[i].get_element_by_id(id2find) #Returned Object
                if ret_obj != empty:
                    return ret_obj

            return empty #If above fails it returns by default empty

    def get_elements_by_tag_name(self, tag):
        found_elems_list = []
        if self.__tag == tag:
            found_elems_list.append(self)
        for i in range(0, len(self.__elements)):
            ret_list = self.__elements[i].get_elements_by_tag_name(tag)
            for j in range(0, len(ret_list)):
                found_elems_list.append(ret_list[j])

        return found_elems_list
        

    def print_tags(self, tab):
        for i in range(0, len(self.__elements)):
            for j in range(0, tab):
                print("\t", end = "")
            print(self.__elements[i].get_tag())
            if len(self.__elements[i].get_elements()) != 0:
                self.__elements[i].print_tags(tab + 1)

    def print_attributes(self, tab):
        for j in range(0, tab):
            print("\t", end = "")
        print(self.__tag, ":", end =  " ")
        for i in range(0, len(self.__attributes)):
            print(self.__attributes[i][0], "=", self.__attributes[i][1], end = " | ")
        print()

        for i in range(0, len(self.__elements)):
            self.__elements[i].print_attributes(tab + 1)

    def print_elements_with_id(self, tab):
        for j in range(0, tab):
            print("\t", end = "")
        print(self.__tag, ":", self.__id)
        for i in range(0, len(self.__elements)):
            self.__elements[i].print_elements_with_id(tab + 1)



# For testing purposes
def main():
    webscr = WebScrap("test.html")
    print(webscr.get_element_by_id("side").get_elements_by_tag_name("div")[0].get_elements_by_tag_name("span")[2].get_elements_by_tag_name("a")[0].get_attribute_value("href"))


if __name__ == "__main__":
    main()
