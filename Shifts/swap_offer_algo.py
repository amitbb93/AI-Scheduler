

def getValuesOfSwapOffer(request):
    swapOrOffer = request.POST['choise']
    return swapOrOffer

def getNameOfTarget(request):
    target_worker = request.POST['target']
    return target_worker