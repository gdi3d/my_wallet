from django.shortcuts import render

# Create your views here.
def dashboard(request):
	context = {'on_dashboard': True}
	return render(request, 'dashboard.html', context)

def money(request):
	operation = request.path.split('/')
	operation = filter(None, operation)[-1]
	context = {'operation': operation}

	return render(request, 'transaction.html', context)

def history(request):
	context = {'on_history': True}
	return render(request, 'history.html', context)

def wallet(request):
	context = {'on_wallets': True}
	return render(request, 'wallet.html', context)

def category(request):
	context = {'on_category': True}
	return render(request, 'category.html', context)