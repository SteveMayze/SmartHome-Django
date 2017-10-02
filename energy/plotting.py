import os
import django
import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import datetime

from matplotlib import style
from django_pandas.io import read_frame

from energy.models import  ResourceEntry
from energy.models import Resource
from energy.models import ResourceValueFactor

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

import matplotlib.dates as mdates


def plot_for_resource( resource, start_date=None, end_date=None):
    print("energy.plotting.plot_for_resource: BEGIN")
    
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ourhouse_site.settings')
    # django.setup()

    if end_date == None:
        end_date = datetime.date.today()
    if start_date == None:
        start_date = end_date + datetime.timedelta(days=-(365 * 2))


    print("Date range {0} - {1}".format( start_date, end_date))

    start_range = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_range = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    res_entity = Resource.objects.filter(slug=resource.lower());
    qs_res = ResourceEntry.objects.filter(resource=res_entity, time_stamp__range=[start_range, end_range])

    style.use('bmh')
    ## style.use('ggplot')

    df_res = qs_res.to_dataframe(fieldnames=['time_stamp', 'value_usage'],  index="time_stamp")
    df_res = df_res.astype(float)

    plt.yscale('log', nonposy='clip')
    plt.xlabel("Months")
    unit = ""
    if resource == "Gas" or resource == "Water":
        unit = "m³"
        ## plt.ylabel("{0} m³".format(resource))
    elif resource == "Electricity":
        unit = "kWh"
        ## plt.ylabel("kWh")
    plt.ylabel("{0} {1}".format(resource, unit))
    plt.title("Resource Usage - {0} {1}".format(resource, unit))
    ## plt.legend()

    fig, ax = plt.subplots( figsize=(8, 6))
    ## fig.tight_layout()
    fig.subplots_adjust(bottom=0.3, right=0.8, top=0.9)

    ax.plot(df_res)
    ax.set_xlabel("Months")
    unit = "kWh"
    if resource == "Gas" or resource == "Water":
        unit = "m³"
        ## ax.set_ylabel("{0} m³".format(resource))
    elif resource == "Electricity":
        unit = "kWh"
        ##ax.set_ylabel("kWh")

    ax.set_ylabel("{0} {1}".format(resource, unit))

    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    yearsFmt = mdates.DateFormatter('%Y-%m')
    ## monthsFmt = mdates.DateFormatter('%m')
    
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_minor_locator(months)
    ax.xaxis.set_major_formatter(yearsFmt)
    ## ax.xaxis.set_minor_formatter(monthsFmt)
    plt.xticks(rotation=45)

        
    ## ax.set_yscale('log', nonposy='clip')
    ## ax.legend(labels=[resource],
    ##          loc=3, borderaxespad=0.)

    canvas = FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    print("energy.pllotting.plot_for_resource: END")


    return response


def plot_summary( start_date=None, end_date=None):
    print("energy.plotting.plot_summary: BEGIN")
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ourhouse_site.settings')
    # django.setup()

    if end_date == None:
        end_date = datetime.date.today()
    if start_date == None:
        start_date = end_date + datetime.timedelta(days=-(365 * 2))


    print("Date range {0} - {1}".format( start_date, end_date))

    gas = Resource.objects.filter(slug="gas");
    qs_gas = ResourceEntry.objects.filter(resource=gas, time_stamp__range=[start_date, end_date])
    elec = Resource.objects.filter(slug="electricity");
    qs_elec = ResourceEntry.objects.filter(resource=elec, time_stamp__range=[start_date, end_date])
    water = Resource.objects.filter(slug="water");
    qs_water = ResourceEntry.objects.filter(resource=water, time_stamp__range=[start_date, end_date])

##    style.use('fivethirtyeight')
    style.use('bmh')

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
    plt.ylabel("Units (kWh/m³)")
    plt.title("Resource Usage")
    plt.legend()

    fig, ax = plt.subplots( figsize=(8, 6))
    ## fig.tight_layout()
    fig.subplots_adjust(bottom=0.3, right=0.8, top=0.9)

    ax.plot(pd_m1)
    ax.set_xlabel("Months")
    ax.set_ylabel("Units (kWh/m³)")
    ax.set_yscale('log', nonposy='clip')
    ax.legend(labels=["Gas", "Elec", "Water"],
              loc=3, borderaxespad=0.)

    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    yearsFmt = mdates.DateFormatter('%y-%m')
    ## monthsFmt = mdates.DateFormatter('%m')
    
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_minor_locator(months)
    ax.xaxis.set_major_formatter(yearsFmt)
    ## ax.xaxis.set_minor_formatter(monthsFmt)
    plt.xticks(rotation=45)

    canvas = FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    print("energy.plotting.plot_summary: END")

    return response
