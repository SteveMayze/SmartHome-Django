from django.shortcuts import render
from energy.plotting import plot_summary

# Create your views here.


def index( request ):

        context_dict = {'pagetitle': 'Our House','pagename': 'Energy',
                        'titlebar': 'Energy' }

        return render(request, 'energy/index.htm', context=context_dict)




def about( request ):
        context_dict = {'pagetitle': 'Our House',
                        'pagename' : 'Energy - About'}
        return render(request, 'about.htm', context=context_dict)



def summary(request) :
        return plot_summary()
