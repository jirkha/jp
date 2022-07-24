import json
from .models import Sale, Product, Transaction
from .forms import SearchForm

import base64
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns
import datetime

### POMOCNÉ FUNKCE ###


### zjistí název prodejního kanálu ze Sale id (pro účely zobrazení DataFrame ve views.py > statistic)
def get_sales_channel_from_id(id):
    sales_channel = Sale.objects.get(id=id)
    return sales_channel


### zjistí název prodejního kanálu z Product id (pro účely zobrazení DataFrame ve views.py > statistic)
def get_product_from_id(id):
    product = Product.objects.get(id=id)
    return product

### funkce potřebná k nastavení zobrazování pandas grafů v templates
def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


### sestaví graf tržeb v požadovaném období vykreslený pomocí views.py > statistic
def get_chart_price(chart_type, data, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(12,3)) ### nastaví velikost grafů
    ### pojmenuje fraf a umístí popisek
    plt.title('Graf prodejů', fontdict={'fontweight': 'bold', 'fontsize': 14})
    ### upraví grafickou podobu grafů dle předdefinovaného stylu (importováno přes "from matplotlib import style")
    plt.style.use('ggplot')
    if chart_type == 'Bar chart':
        print("Bar chart")        
        plt.bar(data.iloc[:, 0], data['total_price'])
        ### popisek vodorovné osy grafu
        plt.xlabel('Období', fontdict={'fontweight': 'bold', 'fontsize': 10})
        ### popisek svislé osy grafu
        plt.ylabel('Tržby [Kč]', fontdict={
                   'fontweight': 'bold', 'fontsize': 10})
        plt.xticks(rotation='45')
        #sns.barplot(x='day_of_sale', y='total_price', data=data)
    elif chart_type == 'Pie chart':
        labels = kwargs.get('labels')
        plt.pie(data=data, x='total_price', labels=labels)
    elif chart_type == 'Line chart':
        print("Line chart")
        plt.plot(data.iloc[:, 0], data['total_price'], 'b.-')
        plt.plot(data.iloc[:, 0],
                 data['total_price'], label="line2") ### line2 na zkoušku - vzor pro budoucí uplatnění
    
    
    plt.tight_layout()
    #plt.legend()
    chart = get_graph()

    return chart


### nastaví správný formát data (bez uvedení času) v Json
def get_json(df):
    """ Small function to serialise DataFrame dates as 'YYYY-MM-DD' in JSON """

    def convert_timestamp(item_date_object):
        if isinstance(item_date_object, (datetime.date, datetime.datetime)):
            return item_date_object.strftime("%Y-%m-%d")

    dict_ = df.to_dict(orient='records')

    return json.dumps(dict_, default=convert_timestamp)


