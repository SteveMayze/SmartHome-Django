import os
import django
import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from matplotlib import style
from django_pandas.io import read_frame

from energy.models import  ResourceEntry
from energy.models import Resource
from energy.models import ResourceValueFactor
from datetime import datetime

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

def plot_summary( ):
    print("plotting.plot_summary: BEGIN")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ourhouse_site.settings')
    django.setup()

    gas = Resource.objects.filter(slug="gas");
    qs_gas = ResourceEntry.objects.filter(resource=gas)
    elec = Resource.objects.filter(slug="electricity");
    qs_elec = ResourceEntry.objects.filter(resource=elec)
    water = Resource.objects.filter(slug="water");
    qs_water = ResourceEntry.objects.filter(resource=water)

##    style.use('fivethirtyeight')
    style.use('ggplot')

    df_gas = qs_gas.to_dataframe(fieldnames=['time_stamp', 'value_usage'],  index="time_stamp")
    df_gas = df_gas.astype(float)

    df_elec = qs_elec.to_dataframe(fieldnames=['time_stamp', 'value_usage'],  index="time_stamp")
    df_elec= df_elec.astype(float)

    df_water = qs_water.to_dataframe(fieldnames=['time_stamp', 'value_usage'],  index="time_stamp")
    df_water = df_water.astype(float)

    pd_m1 = pd.merge(df_gas, df_elec, left_index=True, right_index=True, suffixes=("_gas","_elec"))
    pd_m1 = pd.merge(pd_m1, df_water, left_index=True, right_index=True)
    pd_m1.columns = ['Gas', 'Elec', 'Water']
    ## pd_m1.plot()


    plt.yscale('log', nonposy='clip')
    plt.xlabel("Months")
    plt.ylabel("Units (kWh/m^3)")
    plt.title("Resource Usage")
    plt.legend()

    fig, ax = plt.subplots()
    ax.plot(pd_m1)
    ax.set_xlabel("Months")
    ax.set_ylabel("Units (kWh/m^3)")
    ax.set_yscale('log', nonposy='clip')
    ax.legend(labels=["Gas", "Elec", "Water"],
              loc=3, borderaxespad=0.)

    canvas = FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    print("plotting.plot_summary: END")

    return response
