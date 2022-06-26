from .models import Sale, Product

import base64
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns

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


### sestaví graf vykreslený pomocí views.py > statistic
def get_chart(chart_type, data, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,4)) ### nastaví velikost grafů
    
    if chart_type == 'Bar chart':
        print("bar chart")
        #plt.bar(data['day_of_sale'], data['total_price'])
        sns.barplot(x='day_of_sale', y='total_price', data=data)
    elif chart_type == 'Pie chart':
        labels = kwargs.get('labels')
        plt.pie(data=data, x='total_price', labels=labels)
    elif chart_type == 'Line chart':
        print("line chart")
        plt.plot(data['day_of_sale'], data['total_price'])
    
    plt.tight_layout()
    chart = get_graph()

    return chart
