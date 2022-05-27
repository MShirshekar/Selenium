# directed by: Mohammad Shirshekar

import unittest
from shapely.geometry import Polygon
from selenium import webdriver


class TestClass(unittest.TestCase):
    URL = input("Enter page url: ")
    driver = webdriver.Chrome()
    driver.get(URL)
    rule = 1

    def setUp(self):
        self.URl = TestClass.URL
        self.check = True
        print("\nRule " + str(self.rule) + ": \n")

    def test_1_links_not_images(self):
        image_formats = ['png', 'jpg', 'jpeg', 'svg']
        driver = self.driver
        links = driver.find_elements_by_tag_name("a")
        for link in links:
            if link.get_attribute("href"):
                item = link.get_attribute("href")
                if item is not None:
                    link_format = item.split('.')[-1]
                if link_format in image_formats and item != 'javascript:;':
                    self.check = False
                    print("LINK : " + item)
        self.assertEqual(self.check, True, "Links should not directly target images.")

    def test_2_attributes_deprecated(self):
        elements = self.driver.find_elements_by_xpath('//*')
        deprecated = ['accept', 'align', 'alink', 'allowtransparency', 'archive', 'axis', 'background',
                      'bgcolor', 'border', 'bordercolor', 'cellpadding', 'cellspacing', 'char', 'charoff',
                      'charset', 'classid', 'clear', 'code', 'codebase', 'codetype', 'color', 'compact',
                      'coords', 'datafld', 'dataformatas', 'datapagesize', 'datasrc', 'declare', 'event',
                      'for', 'frame', 'frameborder', 'height', 'hspace', 'ismap', 'language', 'link',
                      'lowsrc', 'marginbottom', 'marginheight', 'marginleft', 'marginright', 'margintop',
                      'marginwidth', 'methods', 'name', 'nohref', 'noshade', 'nowrap', 'profile',
                      'rules', 'scheme', 'scope', 'scrolling', 'shape', 'size', 'standby', 'summary',
                      'target', 'text', 'type', 'urn', 'usemap', 'valign', 'valuetype', 'version',
                      'vlink', 'vspace', 'width']
        for element in elements:
            attributes = self.driver.execute_script(
                'var items = {};'
                ' for (i = 0; i < arguments[0].attributes.length; ++i) {'
                ' items[arguments[0].attributes[i].name] = arguments[0].attributes[i].value'
                ' };'
                ' return items;', element)
            for attribute in attributes:
                if attribute in deprecated:
                    self.check = False
                    print("ID : " + element.id + " || Attribute : " + attribute)
        self.assertEqual(self.check, True, "Attributes deprecated in HTML5 should not be used.")

    def test_3_meta_tag(self):
        elements = self.driver.find_elements_by_tag_name('meta')
        for element in elements:
            item = element.get_attribute('http-equiv')
            if item == "refresh" or item == "redirect":
                self.check = False
                print("ID : " + element.id + " || Attribute : " + item)
        self.assertEqual(self.check, True, "Meta tags should not be used to refresh or redirect.")

    def test_4_style_attribute(self):
        elements = self.driver.find_elements_by_xpath('//*')
        for element in elements:
            item = element.get_attribute("style")
            if item:
                self.check = False
                print("ID : " + element.id + " || Attribute : " + item)
        self.assertEqual(self.check, True, "The ""style"" attribute should not be used.")

    def test_5_identical_links(self):
        identical_links = []
        links = []
        all_links = self.driver.find_elements_by_tag_name('a')
        for i in range(len(all_links)):
            if all_links[i].text:
                links.append(all_links[i])
        for link_first in links:
            link_first_href = link_first.get_attribute('href')
            link_first_text = link_first.text
            for link_second in links:
                link_second_href = link_second.get_attribute('href')
                link_second_text = link_second.text
                if link_first_text == link_second_text and link_first_href != link_second_href:
                    self.check = False
                    if [link_first_text, link_second_href, link_first_href] in identical_links:
                        continue
                    else:
                        identical_links.append([link_first_text, link_first_href, link_second_href])
                        print(" same text : " + link_first_text + "\n different targets:")
                        print("target one: " + link_first_href + "\ntarget two: " + link_second_href + "\n")
        self.assertEqual(self.check, True, "Links with identical texts should have identical targets.")

    def test_6_conflict_input(self):
        window_sizes = [[800, 600], [1024, 768], [1448, 1072], [1600, 1200], [2048, 1536]]
        for iter in range(2):
            if iter == 1:
                self.driver.close()
                self.driver = webdriver.Firefox()
                self.driver.get(self.URL)
            for window_size in window_sizes:
                self.driver.set_window_size(window_size[0], window_size[1])
                inputs = self.driver.find_elements_by_tag_name('input')
                selects = self.driver.find_elements_by_tag_name('select')
                elements = inputs + selects
                coords = []
                for element in elements:
                    element_location = element.location
                    element_size = element.size
                    # (x,y) (x,y + height) (x + width, y + height) ( x + width , y)
                    coords.append([(element_location['x'], element_location['y']), \
                                   (element_location['x'], element_location['y'] + element_size['height']), \
                                   (element_location['x'] + element_size['width'],
                                    element_location['y'] + element_size['height']), \
                                   (element_location['x'] + element_size['width'], element_location['y'])])

                for i in range(len(coords)):
                    poly_first = Polygon(coords[i])
                    for j in range(len(coords)):
                        if coords[i] != coords[j]:
                            poly_second = Polygon(coords[j])
                            if poly_first.intersects(poly_second):
                                self.check = False
                                print('Conflict :' + elements[i].id + '  ||  ' + elements[j].id +
                                      ' Browser :' + self.driver.name + ' ' + str(window_size) + '\n')
        self.assertEqual(self.check, True, "Conflict inputs element or selects elements.")

    def tearDown(self):
        if self.check:
            print("Test Pass.")
        else:
            print("\nTest Failed:)")
        TestClass.rule += 1
        if TestClass.rule == 7:
            self.driver.close()


if __name__ == "__main__":
    unittest.main()
