import base64
import io
import os
from pathlib import Path
from numpy import size

import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.shortcuts import HttpResponse, redirect, render
from matplotlib import pyplot as plt
import seaborn as sb

# Create your views here.
BASE_DIR = Path(__file__).resolve().parent.parent
__login_user_Id = ""
__userlist = {'user': 'user', 'user@gmail.com': '1234567'}
__uploadedFiles = {

}
__global_df = any
__global_df_dataframes = {
    "dataset" : any
}

def index(request):
    return render(request, 'login.html')


def login(request):
    contxt = {"token": 0}
    contxt.update()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('passkey')
        if __userlist.get(username) is None:
            contxt.update({'token': -1})
            return render(request, "login.html", contxt)
        else:
            if __userlist.get(username) == password:
                __login_user_Id = username
                return redirect('/home')
            else:
                contxt.update({'token': 0})
                return render(request, "login.html", contxt)
    else:
        contxt.update({'token': 1})
        return render(request, "login.html", contxt)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('Email')
        passkey = request.POST.get('password')
        if __userlist.get(username) is not None:
            return HttpResponse("User already Exsits")
        else:
            __userlist[username] = passkey
        return redirect('login')
    else:
        return render(request, "register.html")


def homepage(request):
    contxt = {
        "token": 0
    }
    if request.method == "GET":
        return render(request, "userhome.html", contxt)


def upload(request):
    return render(request, "upload.html")


def uploaddatafiles(request):
    contxt = {
        "token": 1
    }
    file = any
    upload = request.FILES['uploadfile']
    print(upload.name)
    acttualp = "media\\" + upload.name
    path =  os.path.join(BASE_DIR , acttualp)
    print(path)
    # filename = request.POST.get('filename')
    fss = FileSystemStorage()
    if os.path.exists(path):
        print("File exists")
        os.remove(path)
        print("file delted")
        file = fss.save(upload.name, upload)
    else:        
        print("File Not exists")
        file = fss.save(upload.name, upload)
    file_url = fss.url(file)
    return render(request, "userhome.html", contxt)


def uploaddata(request):
    contxt = {
        "token": 2
    }
    filename = request.POST.get('filename')
    filelocation = request.POST.get('filelink')
    __uploadedFiles[filename] = [__login_user_Id, filelocation]
    return render(request, "userhome.html", contxt)


def managedata(request):
    list_files = {}
    context = {
        "files": list_files,
        "templatedata": list_files,
        "i": 0
    }
    index = 0
    path = "E:\\Projects_Raju\\python\\Django\\analysis\\media"
    for i in os.listdir(path):
        filename = os.path.basename(i).split('/')[-1]
        pathoffile = path + filename
        context['files'][filename] = {
            "filename": filename, "pathoffile": pathoffile}
    for i in __uploadedFiles:
        context['files'][i] = {"filename": i,
                               "pathoffile": __uploadedFiles[i][1]}
    return render(request, "managedata.html", context)


def deletedataset(request):
    paramter = request.GET['Id']
    path = "E:\\Projects_Raju\\python\\Django\\analysis\\media\\" + paramter
    if os.path.exists(path):
        os.remove(path)
    else:
        __uploadedFiles.pop(paramter)
    return redirect('managedata')
def makegraph(request):
    paramter = request.GET['Id']
    listdata_set = {}   
    list_values = {
        "token_value" : 0,
        "Datasetname" : paramter,
        "loaded_data" : {},
        "nullcolumns" : {},
        "duplicatecolmns" : {},
        "nanvalues" : {},
        "columns" : {},
        "rowcount" : 0,
        "columncount" : 0,
        "totalduplicaterow" : 0
    }
    
    if(request.method == "GET"):
        path = "E:\\Projects_Raju\\python\\Django\\analysis\\media\\"+paramter
        if os.path.exists(path):
            path = "E:\\Projects_Raju\\python\\Django\\analysis\\media\\"+paramter
        else:
            path = paramter
        __global_df = pd.read_csv(path, index_col=False)
        __global_df_dataframes['dataset'] = pd.DataFrame(__global_df)
        dfn = __global_df.isnull().sum()
        _dfn = __global_df.isnull()
        dfd = __global_df.duplicated()
        dfN = __global_df.notna().sum()
        data_html = __global_df.to_html()
        list_values['rowcount'] = len(__global_df.axes[0])
        list_values['columncount'] = len(__global_df.axes[1])
        list_values['totalduplicaterow'] = __global_df.duplicated().sum()
        list_values['loaded_data'] = data_html
        
        for i in _dfn:
            list_values['nullcolumns'][i] = {"Index" : i , "Value" : dfn[i]}
        for i in __global_df.columns:
            list_values['nanvalues'][i] = {"Index" : i , "Value" : dfN[i]}
        
        list_values["dataset"] = __global_df.to_string()
        list_values["duplicatecolmns"] = dfd
        list_values["columns"] = __global_df.columns.values
        # return render(request, "test.html", context)
        print(__global_df.head(5))
        return render(request, "analyzedata.html", list_values)
        
        
def checkuploads(request):
    list_values = {
        "barplotpath" : "",
        "lineplotpath" : "",
        "pieplotpath1" : "",
        "pieplotpath2" : "",
        "distplotpath" : ""
    }
    paramter = request.GET['Id']
    path = "E:\\Projects_Raju\\python\\Django\\analysis\\media\\"+paramter
    if os.path.exists(path):
        path = "E:\\Projects_Raju\\python\\Django\\analysis\\media\\"+paramter
    else:
        path = paramter
    xaxis = request.POST.get('xaxis')
    yaxis = request.POST.get('yaxis')
    
    df = pd.read_csv(path, index_col=False)

    # barplot
    sb.barplot(x = df[xaxis], y = df[yaxis], data=df)
    plt.savefig(os.path.join(BASE_DIR , 'static\graphs\plot1'))
    list_values['barplotpath'] = '/static/graphs/plot1.png'
    
    plt.scatter(df[xaxis].values, df[yaxis].values)
    plt.savefig(os.path.join(BASE_DIR, 'static\graphs\plot4'))
    list_values['lineplotpath'] = '/static/graphs/plot4.png'
    
    #plot1
    
    # piechart
       #chart1
    plt.pie(df[xaxis])
    plt.savefig(os.path.join(BASE_DIR , 'static\graphs\plot2'))
    list_values['pieplotpath1'] = '/static/graphs/plot2.png'
    
    plt.pie(df[yaxis])
    plt.savefig(os.path.join(BASE_DIR, 'static\graphs\plot3'))
    list_values['pieplotpath2'] = '/static/graphs/plot3.png'
    
    #linechart
    
    rdata = df[xaxis].values
    fig, ax = plt.subplots()
    sb.distplot(rdata, ax = ax)
    ax.set_xlim(1 , 200)
    plt.savefig(os.path.join(BASE_DIR, 'static\graphs\plot5'))
    list_values['distplotpath'] = '/static/graphs/plot5.png'
    
    return render(request, "graphs.html", list_values)

def removecolumns(request):
    fss = FileSystemStorage()
    paramter = request.GET['Id']
    param = request.POST.get("fieldsnames")
    path = "E:\\Projects_Raju\\python\\Django\\analysis\\media\\" + paramter
    arraytages = param.split(',')
    print(arraytages)
    df = pd.read_csv(path)
    abc = df.drop(arraytages, axis=1)
    os.remove(path)
    savepath = (os.path.join(path))
    df.to_csv('media', paramter)
    return HttpResponse("lists")
    