from django.shortcuts import render
from energy.plotting import plot_summary
from energy.plotting import plot_for_resource


from energy.forms import ResourceGraphForm
from energy.models import Resource

import datetime

# Create your views here.


def index( request, context_dict=None ):

        if context_dict == None:
                context_dict = {'pagetitle': 'Our House','pagename': 'Energy',
                                'titlebar': 'Energy' }
                resource = "Gas"
                end_date = datetime.date.today()
                start_date = end_date + datetime.timedelta(days = -(365*2))
                
                context_dict["end_date"] = end_date.isoformat()
                context_dict["start_date"] = start_date.isoformat()
                context_dict["resource"] = "3"
        else:
                print("context_dict={0}".format(context_dict))

        print("energy.views: resource={0}, start_date={1}, end_date={2}".format(context_dict["resource"],
                                                                                context_dict["start_date"],
                                                                                context_dict["end_date"]))

        form = ResourceGraphForm( initial={'resource': context_dict["resource"],
                                           'start_date':context_dict["start_date"],
                                           'end_date':context_dict["end_date"]})
        context_dict["resource_graph_form"] = form
        return render(request, 'energy/index.htm', context=context_dict)


def resource_graph( request ):
        print("energy.views.resource_graph BEGIN")
        context_dict = {'pagetitle': 'Our House','pagename': 'Energy',
                                'titlebar': 'Energy' }
        if request.method == 'GET':
                print("energy.views.resource_graph: Processing POST")
                form = ResourceGraphForm( request.GET )
                context_dict["resource"] = request.GET["resource"]
                context_dict["start_date"] = request.GET["start_date"]
                context_dict["end_date"] = request.GET["end_date"]
                return index( request , context_dict)

        print("energy.views.resource_graph END")
        return render (request, 'energy/index.htm', context_dict)

        

def about( request ):
        context_dict = {'pagetitle': 'Our House',
                        'pagename' : 'Energy - About'}
        return render(request, 'about.htm', context=context_dict)



def summary(request) :
        return plot_summary()


def graph_for_resource(request) :
        
        print("energy.views.graph_for_resource BEGIN")
        resource  = request.GET["resource"]
        start_date = request.GET["start_date"]
        end_date = request.GET["end_date"]

        print("energy.views.graph_for_resource: resource={0}, start_date={1}, end_date={2}".format(
                resource, start_date, end_date))

        resource = Resource.objects.filter(id = resource)[0].name

        ## return render (request, 'energy/index.htm', context_dict)
        print("energy.views.graph_for_resource END")
        return plot_for_resource( resource, start_date, end_date)
