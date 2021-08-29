used_categories = ["field-name-field-common-names-display", "field-name-field-datasheet-list", "field-name-field-synonyms-display", "field-name-field-description-display"]
list_Column_names = ["Name", "Unit", "Avg", "SD", "Min", "Max", "Nb"]

# return all common name feed
# if not exist return none
def get_common_names(soap):
    common_name_element = soap.select_one('.field-name-field-common-names-display p')
    if common_name_element is None:
        return None
    return common_name_element.text

# return list for all synonym feed
# if not exist return none
def get_synonyms(soap):
    synonyms_list_paragraph = []

    synonyms_element = soap.select(".field-name-field-synonyms-display p")

    if synonyms_element is None:
        return None
    for p in synonyms_element:
        if len(p.text) > 1:
            synonyms_list_paragraph.append(p.text)
    return synonyms_list_paragraph

# return dictionary of related feed
# if not exist return none
def get_related_feeds(soap):
    related_feed_list = []

    related_feed_elements = soap.select(".view-view-related-feeds a")

    if len(related_feed_elements) == 0:
        return None

    for related in related_feed_elements:

        related_feed_dic = {}

        related_feed_dic['name_href'] = related.text
        related_feed_dic['href'] = related.get('href')
        related_feed_list.append(related_feed_dic)

    return related_feed_dic

# return list of all description
# if not exist return none
def get_description(soap):
    description_list = []

    description_element = soap.select('.field-name-field-description-display p')

    if len(description_element) == 0:
        return None

    for p in description_element:
        if len(p.text) > 1:
            description_list.append(p.text)

    return description_list

# return all information is not above
def get_extra_data(soap):
    list_extra_data = []

    extradata_elements = soap.select('.field')

    for extradata_element in extradata_elements:
        #checking if the category already used by using attrs attribute which holds the classes names
        if(is_used_category(str(extradata_element.attrs)) == False):
            list_extra_data.append(extradata_element.text)

    return list_extra_data

# checking if the name of class name same as used categories
def is_used_category(class_name):
    for category in used_categories:
        if(category in class_name):
            return True
    return False

# return list of table
def get_tables(soap):
    dic_rows_table = []

    table_column = soap.select(".views-field-field-table-content tr")
    for tr in table_column[1:]:
        row = {}
        tds = tr.find_all('td')
        index = 0
        for name_column in list_Column_names:
            row[name_column] = tds[index].text
            index = index + 1

        dic_rows_table.append(row)

    return dic_rows_table

# map extra
# return description of map extra
def get_extra_attributes(soap):
    extra_attributes = {}
    extra_attributes['facebook_link'] = soap.select_one(".art-textblock-1323236578-text a").get("href")
    extra_attributes['icon'] = soap.select_one('[rel="shortcut icon"]').get("href")
    extra_attributes['company_information'] = soap.select_one('.region.region-footer-message p').text
    return extra_attributes
