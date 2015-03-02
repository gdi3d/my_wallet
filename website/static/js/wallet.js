var wallet = {}
wallet = 
{
	ajax: function(url, type, data, callback) {
		
		$.ajax({
			'url': url,
			'contentType': "application/json; charset=utf-8",
    		'dataType': "json",
			'type': type,			
			'data': data,
			beforeSend: function(xhr, settings)
			{
	        	xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
	        },
	        error: function(XMLHttpRequest, textStatus, errorThrown)
	        {
	        	
	        },
	        success: function(data, textStatus)
	        {	        	
	        	callback.success()
	        },
	        complete: function (XMLHttpRequest, textStatus)
	        {

	        },
	        statusCode: {
	        	400: function(XMLHttpRequest)
	        	{
	        		wallet.show_form_error(XMLHttpRequest.responseJSON)
	        	}
	        }

		})
	},
	error_id: '_error_placeholder', // sufix of error fields
	error_placeholder: '<div class="text-danger"></div>', // sufix of error fields
	show_form_error: function(data)
	{
		if(data)
		{
			$.each(data, function(k,v){

				if(!$('#'+k+wallet.error_id).length)
				{
					if($('input[name="'+k+'"]').parent().hasClass('form-group'))
					{						
						$('input[name="'+k+'"]').parent().after(wallet.error_placeholder)
						$('input[name="'+k+'"]').parent().next('div').attr('id', k+wallet.error_id);
					}
					else
					{
						$('input[name="'+k+'"]').after(wallet.error_placeholder);
						$('input[name="'+k+'"]').next('div').attr('id', k+wallet.error_id);
					}
				}

				$('input[name="'+k+'"]').parent().addClass('has-error');
				$('#'+k+wallet.error_id).html(v)
			});			
		}
	},
	clear_errors: function(data)
	{
		$('div[id*="'+wallet.error_id+'"').html('');
		$('.has-error').removeClass('has-error');
		$('div[role="alert"').remove();
	},
	categories: {},
	wallets: {},
	init: function()
	{
		wallet._categories()
		wallet._wallets()
		$('#amount').numeric({ decimalPlaces: 4 });
	},
	_categories: function()
	{		
		$.get( "/api/v1/category/", function(data) { 
			wallet.categories = data
			$.each(data.results, function(k,v){
				
				$('#category').append('<option value="'+v.id+'">'+v.name+'</option>')
			})
		})		

	},
	_wallets: function(callback)
	{
		$.get("/api/v1/wallet/", function(data) { 
			wallet.wallet = data

			$.each(data.results, function(k,v)
			{				
				$('#wallet').append('<option value="'+v.id+'">'+v.name+'</option>')
			})

			if(callback !== undefined)
			{
				callback()
			}
		})		
	}
}




wallet.main_actions = {
	_common: function()
	{
		$('#main_page').hide();
		$('#form_page').show()
	},
	income: function()
	{
		wallet.main_actions._common()
		$('#action_msg').html('Hello Money <i class="fa fa-smile-o"></i>').removeClass('text-danger').addClass('text-success');
		$('#action_amount').html('Amount earn').removeClass('text-danger').addClass('text-success')
		$('#action').val('+');
		$('#amount_addon').html('+ $');
	},
	expense: function()
	{
		wallet.main_actions._common()		
		$('#action_msg').html('Bye Money <i class="fa fa-frown-o"></i>').addClass('text-danger').removeClass('text-success');
		$('#action_amount').html('Amount lost').addClass('text-danger').removeClass('text-success')
		$('#action').val('-');
		$('#amount_addon').html('- $');
	},	
	save: function()
	{
		var callback =
		{
			success: function(data, textStatus)
			{
				msg = 'The data was saved'
				wallet.main_actions.add_message('success', msg)
				$('#transaction_form')[0].reset();
			}
		}

		data = {
			'item':
			{
				'amount': $('#action').val() + $('#amount').val(),
				'category_id': $('#category').val(),
				'note': $('#note').html()
			},
			'transaction': {
				'date': $('#date').val(),
				'wallet_id': $('#wallet').val()	
			}			
		}	

		wallet.clear_errors();
		wallet.ajax('/api/v1/transactions/', 'POST', JSON.stringify(data), callback)		
	},
	transactions: function()
	{
		$.get( "/api/v1/transactions/", function(data) { 
			wallet.wallet = data

			$.each(data.results, function(k,v)
			{				
				$('#wallet').append('<option value="'+v.id+'">'+v.name+'</option>')
			}) 
		})
	},
	add_message: function(type, msg)
	{
		switch(type)
		{
			case 'success':
				msg = '<strong>Done!</strong> '+msg
			break;
			case 'info':
				msg = '<strong>Heads up!</strong> '+msg
			break;
			case 'warning':
				msg = '<strong>Warning!</strong> '+msg
			break;
			case 'danger':
				msg = '<strong>Oh snap!</strong> '+msg
			break;
		}

		html = '<div class="alert alert-'+type+'" role="alert" style="margin-top:10px">'+msg+'</div>'
		$('#main_content').prepend(html)
		$('html, body').animate({ scrollTop: 0 }, 'fast');
	}
}