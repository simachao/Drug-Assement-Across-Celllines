

import statistics
import operator

import matplotlib.pyplot as plt
import numpy as np



plots_folder = 'plots/'

#%% functions
def barplot(D,measureType):
    
    global plots_folder
    
    allkeys = D.keys()
    #dictValues = dict.fromkeys(allkeys)
    dictMedian = dict.fromkeys(allkeys)
    dictMax = dict.fromkeys(allkeys)
    dictMin = dict.fromkeys(allkeys)
    dictNumCells = dict.fromkeys(allkeys)
    
    for key in allkeys:
        values = D[key]
        #print(type(values))
        #print(values)
        #dictValues[key]= values
        
        dictMedian[key] = statistics.median(values)
        dictMax[key] = max(values)
        dictMin[key] = min(values)
        dictNumCells[key] = len(values)

    #print(dictNumCells)
    numAllCelllines = max(list(dictNumCells.values()))
    
    sortedDict_byMedian = sorted(dictMedian.items(), key=operator.itemgetter(1), reverse=True)
    #print(type(sortedDict_byMedian))
    #print(sortedDict_byMedian)
    sortedDict_byMedian = dict(sortedDict_byMedian)
    
    
    errbars = np.empty([2,len(allkeys)])

    counter = 0
    for key in sortedDict_byMedian.keys():
        #print(key)
        errbars[0,counter] = dictMedian[key] - dictMin[key]
        errbars[1,counter] = dictMax[key] - dictMedian[key]
        counter += 1

    #print(errbars)

    fig, ax = plt.subplots(figsize=(numAllCelllines, 10))

    #plt.bar()  
    rects = ax.bar(range(len(sortedDict_byMedian)), sortedDict_byMedian.values(), align='center',yerr = errbars)
    
    
    #plt.xticks(range(len(sortedDict_byMedian)), list(sortedDict_byMedian.keys()), rotation='vertical')
    plt.xticks(range(len(sortedDict_byMedian)), list(sortedDict_byMedian.keys()))
    plt.xticks(rotation=45)
    
    
    #plt.show()
#    rects = ax.bar(range(len(sortedDict_byMedian)), sortedDict_byMedian.values(), align='center',yerr = errbars)
#    for rect in rects:
#        height = rect.get_height()
#        ax.text(rect.get_x() + rect.get_width()/2., 1.05,
#                'T',ha='center', va='bottom')
    
    allSortedKeys = list(sortedDict_byMedian.keys())
    for i in range(0,len(rects)):
        key = allSortedKeys[i]
        if dictNumCells[key] < numAllCelllines:
            #rects[i].set_facecolor('r')
            rects[i].set_alpha(0.5)
            ax.text(i+0.2, 0.05,str(dictNumCells[key]),ha='center', va='bottom')
        else:
            rects[i].set_alpha(0.85)
        
    plt.title('{0} (#of celllines total: {1})'.format(measureType,numAllCelllines))
            
    # add a line
    if measureType == 'AUC':
        plt.ylabel('Area Under Curve')
        plt.plot([0,len(rects)],[1, 1], linewidth=2,color='r',linestyle=':')
        ax.text(len(rects)+0.2, 1,'100% AUC',ha='left', va='bottom')
    elif measureType == 'Last Time Point':
        plt.ylabel('Apop Percentage')
        plt.plot([0,len(rects)],[1, 1], linewidth=2,color='r',linestyle=':')
        ax.text(len(rects)+0.2, 1,'100% Death',ha='left', va='bottom')
    else:
        plt.ylabel('Hours')
        plt.plot([0,len(rects)],[24, 24], linewidth=2,color='r',linestyle=':')
        ax.text(len(rects)+0.2, 24,'24 hour',ha='left', va='bottom')
        plt.plot([0,len(rects)],[-1, -1], linewidth=2,color='r',linestyle=':')
        ax.text(len(rects)+0.2, -1,'Never Occurred',ha='left', va='bottom')
    
    plt.plot()
    plt.savefig(plots_folder+measureType+'_boxplot.png')
    



def violinplot(D,measureType):
    
    global plots_folder
    
    allkeys = D.keys()
    dictValues = dict.fromkeys(allkeys)
    dictMedian = dict.fromkeys(allkeys)
    dictMax = dict.fromkeys(allkeys)
    dictMin = dict.fromkeys(allkeys)
    dictNumCells = dict.fromkeys(allkeys)
    
    for key in allkeys:
        values = D[key]
        #print(type(values))
        #print(values)
        #dictValues[key]= values
        dictValues[key]= [float(x) for x in values]
        
        dictMedian[key] = statistics.median(values)
        dictMax[key] = max(values)
        dictMin[key] = min(values)
        dictNumCells[key] = len(values)

    #print(dictNumCells)
    numAllCelllines = max(list(dictNumCells.values()))
    
    sortedDict_byMedian = sorted(dictMedian.items(), key=operator.itemgetter(1), reverse=True)
    #print(type(sortedDict_byMedian))
    #print(sortedDict_byMedian)
    sortedDict_byMedian = dict(sortedDict_byMedian)
    
    
    errbars = np.empty([2,len(allkeys)])

    counter = 0
    for key in sortedDict_byMedian.keys():
        #print(key)
        errbars[0,counter] = dictMedian[key] - dictMin[key]
        errbars[1,counter] = dictMax[key] - dictMedian[key]
        counter += 1

    #print(errbars)

    fig, ax = plt.subplots(figsize=(numAllCelllines, 10))

    #plt.bar()  
#    rects = ax.bar(range(len(sortedDict_byMedian)), sortedDict_byMedian.values(), align='center',yerr = errbars)
    
    data = dictValues.values()
    #pos = [x for x in range(len(sortedDict_byMedian))]
    
    sortedKeys = list(sortedDict_byMedian.keys())
    dataKeys = list(dictValues.keys())
    #print(sortedKeys)
    #print(dataKeys)
    
    #pos = [x for x in range(len(sortedDict_byMedian))]
    pos = [np.where([sk ==  dataKeys[idx] for sk in sortedKeys])[0][0] for idx in range(len(dataKeys))]
    #print(pos)

    rects = ax.violinplot(data,pos,showmedians=True)
    #print(type(rects))
    
    #plt.xticks(range(len(sortedDict_byMedian)), list(sortedDict_byMedian.keys()), rotation='vertical')
    plt.xticks(range(len(sortedDict_byMedian)), list(sortedDict_byMedian.keys()))
    plt.xticks(rotation=45)
    
    

    
    allSortedKeys = sortedKeys
    for i in range(0,len(allSortedKeys)):
        key = allSortedKeys[i]
        rect_pos = pos.index(i)
        if dictNumCells[key] < numAllCelllines:
            #rects['bodies'][rect_pos].set_facecolor('r')
            rects['bodies'][rect_pos].set_alpha(0.5)
            ax.text(i+0.2, 0.05,str(dictNumCells[key]),ha='center', va='bottom')
        else:
            #pass
            rects['bodies'][rect_pos].set_alpha(0.85)
        
    plt.title('{0} (#of celllines total: {1})'.format(measureType,numAllCelllines))
            
    # add a line
    xmin,xmax = ax.get_xlim()
    if measureType == 'AUC':
        plt.ylabel('Area Under Curve')
        plt.plot([0,xmax],[1, 1], linewidth=2,color='r',linestyle=':')
        ax.text(xmax, 1,'100% AUC',ha='left', va='bottom')
    elif measureType == 'Last Time Point':
        plt.ylabel('Apop Percentage')
        plt.plot([0,xmax],[1, 1], linewidth=2,color='r',linestyle=':')
        ax.text(xmax, 1,'100% Death',ha='left', va='bottom')
    else:
        plt.ylabel('Hours')
        plt.plot([0,xmax],[24, 24], linewidth=2,color='r',linestyle=':')
        ax.text(xmax, 24,'24 hour',ha='left', va='bottom')
        plt.plot([0,xmax],[-1, -1], linewidth=2,color='r',linestyle=':')
        ax.text(xmax, -1,'Never Occurred',ha='left', va='bottom')
    
    plt.plot()
    plt.savefig(plots_folder+measureType+'_violin.png')
