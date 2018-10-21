import requests
from bs4 import BeautifulSoup
import re
from sklearn import tree, preprocessing


class CarPrice:
    # give the url based on your country .. obviously car prices are different
    # in different countries!!!

    def souping_data(car_website_url):
        try:
            request = requests.get(car_website_url)
        except Exception as err:
            print(err)
        soup = BeautifulSoup(request.text, 'html.parser')
        # you may need to change this search option based on the website you're
        # getting the data from!
        all_data = soup.find_all('div', {'class': 'listdata'})
        my_list = list()
#        for test purposes and in case you want the results on file
#        my_file = open('/home/doctorcode7/Desktop/file.txt', 'w')
        for data in range(len(all_data)):
            car_h2_details = all_data[data]
            car_h2_details = car_h2_details.find('h2')
            car_h2_details = car_h2_details.text
            car_h2_details = re.sub(r'\s+', ' ', car_h2_details)
            car_h2_details = car_h2_details.strip()
            car_h2_details = car_h2_details.split('،')
            if car_h2_details[0].isdigit():
                date_of_manufacture = car_h2_details[0]
                brand = car_h2_details[1]
                model = car_h2_details[2]
            else:
                continue
            price = all_data[data]
            price = price.find('span', {'itemprop': 'price'})
            if price is None:
                continue
            else:
                price = price.get('content')
            if price == '0':
                continue
            kilometers = all_data[data]
            kilometers = kilometers.find('p', {'class': 'price hidden-xs'})
            kilometers = kilometers.text
    #        for test purpose (file)
            # my_file.write("%s\n" % date_of_manufacture)
            # my_file.write("%s\n" % model)
            # my_file.write("%s\n" % brand)
            # my_file.write("%s\n" % price)
            # my_file.write("%s\n" % kilometers)

            my_list.extend([(date_of_manufacture, brand, model, kilometers,
                             price)])
    #    my_file.close()
        return my_list

    def predict_car_price(my_list, new_data):
        x = list()
        y = list()
        for row in my_list:
            x.append(row[:4])
            y.append(row[-1])
        le = preprocessing.LabelEncoder()
        for i in range(len(x)):
            x[i] = le.fit_transform(x[i])
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(x, y)
        for i in range(len(new_data)):
            new_data[i] = le.fit_transform(new_data[i])
        return clf.predict(new_data)
