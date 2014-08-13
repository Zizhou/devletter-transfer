from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from submit.models import Game, Developer
from transfer.models import GameForm, DeveloperForm
from transfer.spreadsheet import Spreadsheet
from transfer.settings import settings

# Create your views here.

@login_required
def main_page(request):
    #process input
    if request.method == 'POST':
        #and now I know the RIGHT way to use prefixes on this end
        gform = GameForm(request.POST, prefix = 'game')
        dform = DeveloperForm(request.POST, prefix = 'dev')
        
        dtemp = Developer()
        gtemp = Game()
        #if this one is valid, by definition, the gform can't be
        #so it's neccessarry to make input the new dev number
        if dform.is_valid():
            dtemp = dform.save()
            print 'id is '
            print type(dtemp) 
            #deep copy for mutable QueryDict
            temp_dict = request.POST.copy()
            temp_dict.__setitem__('game-developer', dtemp.id)
            for i in temp_dict:
                print i
                print temp_dict[i]
            #should be valid now, regardless?
            gform = GameForm(temp_dict, prefix  = 'game')
        #valid either automatically, or from dev-form processing
        if gform.is_valid():
            gtemp = gform.save()
        else:
            #if this triggers, I messed up somewhere
            return HttpResponse('You done fucked up now')

        return HttpResponseRedirect('/transfer/')
    #get next record and await approval
    try:
        row = Spreadsheet(**settings).get_next_row()
    except:
        return HttpResponse('Hey, it looks like your error catching worked. Nice one.')
    if row == None:
        return HttpResponse('All done for now!')
    g_row = game_row_process(row)
    d_row = dev_row_process(row)
    gform = GameForm(prefix = 'game', initial = g_row)
    dform = DeveloperForm(prefix = 'dev', initial = d_row)
    context = {
    'gform' : gform,
    'dform' : dform,
    }
    return render(request, 'transfer/form.html', context)

#helpers to process spreadsheet input into the appropriate forms
#very hardcoded much bad practice
def game_row_process(row):
    output = {'notes':'','lastyear':True,}
    for i in row.custom:
        if i[0:5] == 'game-':
            if i[5:9] == 'note':
                output['notes'] = output['notes'] + row.custom.get(i).text
            else:
                output[i[5:]] = row.custom.get(i).text
    return output

def dev_row_process(row):
    output = {}
    for i in row.custom:
        if i[0:4] == 'dev-':
            if i[4:8] == 'note':
                output['notes'] = output['notes'] + '\n' + row.custom.get(i).text
            else:
                output[i[4:]] = row.custom.get(i).text
    return output
