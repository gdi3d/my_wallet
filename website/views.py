from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
	return render(request, 'home.html')

@login_required
def dashboard(request):
	context = {'on_dashboard': True}
	return render(request, 'dashboard.html', context)

@login_required
def money(request, pk=None):
	
	if not pk:
		pk = ''
		
	context = {'on_transaction': True, 'pk': pk}

	return render(request, 'transaction.html', context)

@login_required
def history(request):
	context = {'on_history': True}
	return render(request, 'history.html', context)

@login_required
def wallet(request):
	context = {'on_wallets': True}
	return render(request, 'wallet.html', context)

@login_required
def category(request):
	context = {'on_category': True}
	return render(request, 'category.html', context)