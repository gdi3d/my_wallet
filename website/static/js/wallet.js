var w = {}
/**
 * common functions
 */
w = 
{
	/**
	 * ajax calls. It's a wrapper for jQuery.ajax()
	 * @param  {string}		url      Request url
	 * @param  {string}		type     Request call type (POST, PUT, GET, etc)
	 * @param  {mixed}		data     Data to send on the request
	 * @param  {Function} 	callback Callback
	 * 
	 */
	ajax: function(url, type, data, callback) {
		
		$.ajax({
			'url': url,
			'contentType': "application/json; charset=utf-8",
    		'dataType': "json",
			'type': type,			
			'data': data,
			beforeSend: function(xhr, settings)
			{
				w.clear_errors();
	        	xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
	        },
	        error: function(XMLHttpRequest, textStatus, errorThrown)
	        {
	        	if(callback.hasOwnProperty('error'))
	        	{
	        		callback.error(XMLHttpRequest, textStatus, errorThrown)	        		
	        	}
	        },
	        success: function(data, textStatus)
	        {
	        	if(callback.hasOwnProperty('success'))
	        	{
	        		callback.success(data, textStatus)	        		
	        	}
	        },
	        complete: function (XMLHttpRequest, textStatus)
	        {
	        	if(callback.hasOwnProperty('complete'))
	        	{
	        		callback.complete(XMLHttpRequest, textStatus)	        		
	        	}
	        },
	        statusCode: {
	        	400: function(XMLHttpRequest)
	        	{	        		
	        		w.show_form_error(XMLHttpRequest.responseJSON)
	        	}
	        }

		})
	},
	/**
	 * Process the errors for django rest framework
	 * and create an array map var[field] = error to be
	 * used on show_form_error function
	 * @type {Array}
	 */
	_api_response_fields_tmp: new Array(),
	api_response_fields: new Array(),
	recursiveIteration: function(object)
	{
	    for (var property in object) {
	        if (object.hasOwnProperty(property)) {
	            if (typeof object[property] == "object"){
					w._api_response_fields_tmp.push(property)
	                w.recursiveIteration(object[property]);
	            }else{
	                //found a property which is not an object, check for your conditions her            	
	                if(w._api_response_fields_tmp.length > 0)
	                {	                	
						field_id = w._api_response_fields_tmp.join('_')
						w.api_response_fields[field_id] = object
						w._api_response_fields_tmp = new Array()
	                }
	            }
	        }
	    }
	},
	error_id: '_error_placeholder', // sufix of error fields
	error_placeholder: '<div class="text-danger"></div>',
	/**
	 * Show the errors from the api on the forms
	 * @param  {object} data The response from the api
	 */
	show_form_error: function(data)
	{
		if(data)
		{
			// convert the response into a mapped array
			w.recursiveIteration(data)
			for(var k in w.api_response_fields)
			{								
				v = w.api_response_fields[k]

				if(!$('#'+k+w.error_id).length)
				{
					if($(':input[name="'+k+'"]').parent().hasClass('form-group'))
					{						
						$(':input[name="'+k+'"]').parent().after(w.error_placeholder)
						$(':input[name="'+k+'"]').parent().next('div').attr('id', k+w.error_id);
					}
					else
					{
						$(':input[name="'+k+'"]').after(w.error_placeholder);
						$(':input[name="'+k+'"]').next('div').attr('id', k+w.error_id);
					}
				}

				$(':input[name="'+k+'"]').parent().addClass('has-error');				
				
				$('#'+k+w.error_id).html(v[0])
			}			
		}
	},
	/**
	 * Clean up all the errors on the form
	 */
	clear_errors: function()
	{
		$('div[id*="'+w.error_id+'"').html('');
		$('.has-error').removeClass('has-error');
		$('div[role="alert"]').remove();
		w.api_response_fields = new Array()
		w._api_response_fields = new Array()
	},
	/**
	 * Show an alert message
	 * @param {string} type Type of error to show
	 * @param {string} msg  Message
	 */
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

		html = '<div class="alert alert-'+type+' alert-dismissible" role="alert" style="margin-top:10px"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+msg+'</div>';

		$('#main_content').prepend(html);
		$('html, body').animate({ scrollTop: 0 }, 'fast');
	},
	categories: {},
	wallets: {},
	/**
	 * Return all the wallets
	 * @param  {Function} callback callback
	 */
	_wallets_ko: function(callback)
	{
		$.get("/api/v1/wallet/", function(data) { 
			
			callback(data.results)
		})
	},
	DECIMAL_SYMBOL: ',',
	DECIMAL_PLACES: 2, // max 4
	THOUSAND_SYMBOL: '.',
	CURRENCY_SYMBOL: '$',
	/**
	 * Format numbers
	 * @param  {number} number                  The number to be formatted
	 * @param  {boolean} include_currency_symbol Prepend the currency symbol
	 * @return {string}                         The formatted number
	 */
	format_number: function(number, include_currency_symbol)
	{
		if(include_currency_symbol)
		{
			n = accounting.formatMoney(number, w.CURRENCY_SYMBOL, w.DECIMAL_PLACES, w.THOUSAND_SYMBOL, w.DECIMAL_SYMBOL);	
		}
		else
		{
			n = accounting.formatMoney(number, '', w.DECIMAL_PLACES, w.THOUSAND_SYMBOL, w.DECIMAL_SYMBOL);	
		}

		return n;		
	}
}

/**
 * Create an alert dialog with two buttons
 * 
 */
w.alert =
{
    create: function()
    {
    	this.alert_id 			= 'alert_dialog_'+Date.now()
        this.ok_function        = false;
        this.cancel_function    = "$('#"+this.alert_id+"').alert('close')";
        this.ok_label;
        this.cancel_label;
        this.head_text;
        this.body_text;
        this.type_class         = 'alert-danger';
        this.target             = '#main_content';

        this.show = function()
        {
        	var self = this;

        	alert_html = '<div class="alert alert-dismissible fade in" role="alert" id="alert_dialog"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">×</span></button><h4 class="alert-heading"></h4><p class="alert-body"></p><p><button type="button" class="btn btn-success alert-button-ok btn-sm">Take this action</button>&nbsp;<button type="button" class="btn btn-default alert-button-cancel">Or do this</button></p></div>';

            $(self.target).prepend(alert_html);            
            $('#alert_dialog').attr('id', self.alert_id);
            
            alert_selector = '#'+self.alert_id;

            $(alert_selector).addClass(self.type_class);
            
            $(alert_selector+' .alert-heading').html(self.head_text);
            $(alert_selector+' .alert-body').html(self.body_text);

            if(self.ok_label !== undefined)
            {
                $(alert_selector+' .alert-button-ok').html(self.ok_label);
                $(alert_selector+' .alert-button-ok').click(function(){ eval(self.ok_function) });
            }
            else
            {
                $(alert_selector+' .alert-button-ok').hide();
            }

            if(self.cancel_label !== undefined)
            {
                $(alert_selector+' .alert-button-cancel').html(self.cancel_label);
                $(alert_selector+' .alert-button-cancel').click(function(){ eval(self.cancel_function) });
            }
            else
            {
                $(alert_selector+' .alert-button-cancel').hide();
            }

            $(self.target).fadeIn();

            $('html, body').animate({ scrollTop: 0 }, 'fast');
        };
    }
};

/**
 * Transaction view
 *
 */
w.transaction_view =
{
	model: {},
	_wallets: {},
	transaction_type: '',
	/**
	 * Initializate the view
	 * @param  {integer} id The transaction id to be edited
	 */
	init: function(id)
	{
		// Bindings for knockout js
		w._wallets_ko(function(wallets)
		{
			w.transaction_view._wallets = wallets;

			w.category_view._categories_list(function(categories)
			{
				// defines the view object model
				w.transaction_view.model = ko.mapping.fromJS(
				{
					'item': {
						'amount':null, 'note': '', 'id': '', 'category': {'id': 0}
					},
					'id': '',
					'date': '',
					'wallet': {'id':''},
					'wallets': w.transaction_view._wallets,
					'categories': categories,
				});

				ko.applyBindings(w.transaction_view.model);				
				
				// load a transaction to be edited
				if(typeof id !== 'undefined' && id !== '')
				{
					w.transaction_view.load(id)
				}
				else if(w.transaction_view.model.wallets().length <  2)
				{
					// if there's only one wallet, let's autoselect it					
					w.transaction_view.model.wallet.id(w.transaction_view.model.wallets()[0].id())
				}
			})						
		});		

		// buttons bindings
		$('#save').click(function(){ w.transaction_view.save() });

		$('#action_in').click(function(){ w.transaction_view.income()});
		$('#action_out').click(function(){ w.transaction_view.expense()});

		$('#date').datepicker({
		    format: 'yyyy/mm/dd',
		    todayBtn: "linked",
		    todayHighlight: true
		});

		$('#amount').numeric({ decimalPlaces: w.DECIMAL_PLACES });
		$('#amount').keyup(function()
			{ 
				val = $(this).val();

				if(val.search('-') > -1)
				{
					w.transaction_view.expense();
				}
				else
				{
					w.transaction_view.income();
				}
			});

		$('#currency').html(w.CURRENCY_SYMBOL);
	},
	/**
	 * Set text for income money
	 */
	income: function()
	{
		$('#action_msg').html('Hello Money <i class="fa fa-smile-o"></i>').removeClass('text-danger').addClass('text-success');
		$('#action_item_amount').html('Amount earn').removeClass('text-danger').addClass('text-success')
	},
	/**
	 * Set text for outcome money
	 */
	expense: function()
	{
		$('#action_msg').html('Bye Money <i class="fa fa-frown-o"></i>').addClass('text-danger').removeClass('text-success');
		$('#action_item_amount').html('Amount lost').addClass('text-danger').removeClass('text-success')
		
	},
	/**
	 * Save the transaction
	 */
	save: function()
	{
		var callback =
		{
			success: function(data, textStatus)
			{
				msg = 'The data was saved'
				w.add_message('success', msg)				
				w.transaction_view.load(data.id)
			},
			error: function()
			{
				msg = 'Shit!, something is broken. Nothing was saved :(';
				w.add_message('warning', msg)
			}
		}

		// set the values on the view model
		var category = w.transaction_view.model.item.category
		if(category === null)
		{
			var category_id = null
		}
		else
		{
			var category_id = w.transaction_view.model.item.category.id()
		}

		var wallet_id = w.transaction_view.model.wallet.id()
		if(typeof wallet_id == 'undefined')
		{
			var wallet_id = null
		}

		data = {
			'item':
			{
				'amount': w.transaction_view.model.item.amount(),
				'category_id': category_id,
				'note': w.transaction_view.model.item.note(),
				'id': w.transaction_view.model.item.id()
			},			
			'date': w.transaction_view.model.date(),
			'wallet_id': wallet_id,
			'id': w.transaction_view.model.id()
						
		}
		
		id = w.transaction_view.model.id();

		// send the data to the endpoint
		if(id > 0)
		{
			w.ajax('/api/v1/transactions/'+id, 'PUT', JSON.stringify(data), callback)
		}
		else
		{
			w.ajax('/api/v1/transactions/', 'POST', JSON.stringify(data), callback)
		}
	},
	/**
	 * Load a transaction
	 * @param  {integer} id The id to be edited
	 * 
	 */
	load: function(id)
	{
		$.get("/api/v1/transactions/"+id, function(data)
		{
			if(data.item.amount < 0)
			{
				w.transaction_view.expense()
			}
			else
			{
				w.transaction_view.income()	
			}

			// change the date separator from - to /
			data.date = data.date.replace(/-/g, '/')

			// map the api response to the view model
			ko.mapping.fromJS(data, w.transaction_view.model);			
		});
	}
}

/**
 * Wallet view
 */
w.wallet_view =
{
	model: {},
	/**
	 * Initializate the view	 
	 */
	init: function()
	{
		w._wallets_ko(function(wallets)
		{
			// defines the view object model
			w.wallet_view.model = ko.mapping.fromJS({
				'name':null,
				'id':null,
				'initial_amount':null,
				'note':null,
				'wallets': wallets
			});

			ko.applyBindings(w.wallet_view.model);
			w.wallet_view.load(w.wallet_view.model.id())			
		})		

		// buttons bindings
		$('#save').click(function(){ w.wallet_view.save(); });
		$('#new').click(function(){ w.wallet_view.new() });
		$('#del').click(function(){ w.wallet_view.del() });

		$('#initial_amount').numeric({ decimalPlaces: w.DECIMAL_PLACES });

		$('#currency').html(w.CURRENCY_SYMBOL);
		
	},
	/**
	 * Trigger a change event on the wallet dropdown
	 * @param  {object} data
	 * @param  {object} event
	 */
	change_event: function(data, event)
	{
		if(data.id() !== undefined)
		{
			$('#del').show();
			w.wallet_view.load(data.id())		
		}
	},
	/**
	 * Loads a wallet
	 * @param  {integer} id The id of the load to be loaded
	 */
	load: function(id)
	{
		if(id == undefined)
		{
			return
		}

		$('#del').show();

		// call the endpoint
		$.getJSON("/api/v1/wallet/"+id, function(data)
		{
			// map the api response to the view model
			ko.mapping.fromJS(data, w.wallet_view.model);
		});
	},
	/**
	 * Create a new wallet
	 */
	new: function()	
	{
		$('#wallets_form')[0].reset(); 
		$('#wallet').val(0);
		$('#del').hide();
		w.wallet_view.model.initial_amount('0.00')
		w.wallet_view.model.id(0)
	},
	/**
	 * Save the wallet
	 */
	save: function()
	{
		var callback =
		{
			success: function(data, textStatus)
			{
				msg = 'The data was saved'
				w.add_message('success', msg)
				
				w._wallets_ko(function(wallets_data)
				{
					data.wallets = wallets_data					
					ko.mapping.fromJS(data, w.wallet_view.model)
					// for some reason i've to force this value to change
					// the select the new option on the dropdown
					// this also end up adding a new request
					w.wallet_view.load(data.id)
				})
			},
			error: function()
			{
				msg = 'Shit!, something is broken. Nothing was saved :(';
				w.add_message('warning', msg)
			}
		}

		// conver the view model into a js object
		data = ko.toJS(w.wallet_view.model);
		
		id = data.id
		
		// remove knockout keys
		delete data.__ko_mapping__;		
		data = JSON.stringify(data);
		w.clear_errors();

		// send the data to the endpoint
		if(id > 0)
		{			
			w.ajax('/api/v1/wallet/'+id, 'PUT', data, callback)
		}
		else
		{
			w.ajax('/api/v1/wallet/', 'POST', data, callback)
		}		
	},
	/**
	 * Show the delete alert
	 */
	del: function()
	{
		w.clear_errors()
		var wallet_name = $('#wallet option:selected').text();

		// create the alert dialog object
		var alert = new w.alert.create();
		alert.ok_label = 'Yes, delete it';
		alert.cancel_label = 'No, don\'t delete it!!';
		alert.head_text = 'Watch out!!';
		alert.body_text = 'Are you sure you want to delete the wallet <strong>'+wallet_name+'?</strong>. All the information saved to this wallet will be deleted too';
		alert.ok_function = 'w.wallet_view._del()';
		alert.show();
	},
	/**
	 * Delete the wallet
	 */
	_del: function()
	{
		var callback =
		{
			success: function(data, textStatus)
			{
				msg = 'The wallet was deleted'
				w.add_message('success', msg)
				$('#wallet').find('option[value="'+id+'"]').remove()
				$('#wallets_form')[0].reset(); 
				w.wallet_view.load($('#wallet option').first().val())			
			},
			error: function()
			{
				msg = 'Shit!, something is broken. Nothing was deleted :(';
				w.add_message('warning', msg)
			}
		}

		id = w.wallet_view.model.id()

		// call the endpoint to delete the wallet
		w.ajax('/api/v1/wallet/'+id, 'DELETE', {}, callback)
	}
}

/**
 * Category view
 */
w.category_view =
{
	model: {},
	/**
	 * Get all the categories
	 * @param  {Function} callback [description]
	 */
	_categories_list: function(callback)
	{
		// TODO make recursive calls insted of settings page_size of 500
		$.get("/api/v1/category/?page_size=500", function(data)
		{ 			
			callback(data.results)
		});
	},
	/**
	 * Initializate the view
	 */
	init: function()
	{
		w.category_view._categories_list(function(categories)
		{
			// set the view model
			w.category_view.model = ko.mapping.fromJS({
				'name':null,
				'id':null,
				'categories': categories
			});

			ko.applyBindings(w.category_view.model);
			w.category_view.load(w.category_view.model.id())
		});

		// buttons bindings
		$('#save').click(function(){ w.category_view.save(); });
		$('#new').click(function(){ w.category_view.new() });
		$('#del').click(function(){ w.category_view.del() });
	},
	/**
	 * Triggered when selecting a category from the dropdown
	 * @param  {object} data 
	 * @param  {object} event 
	 */
	change_event: function(data, event)
	{
		w.category_view.load(data.id())
	},
	/**
	 * Load the category
	 * @param  {integer} id The id of the category to load
	 */
	load: function(id)
	{
		if(id === undefined)
		{
			return
		}

		$('#del').show();

		$.getJSON("/api/v1/category/"+id, function(data)
		{
			// map the api response to the view model
			ko.mapping.fromJS(data, w.category_view.model);
		});
	},
	/**
	 * Create a new category
	 */
	new: function()
	{
		$('#category_form')[0].reset(); 
		$('#category').val(0);
		w.category_view.model.id(0)	
		$('#del').hide()
	},
	/**
	 * Save the category
	 */
	save: function()
	{
		var callback =
		{
			success: function(data, textStatus)
			{
				msg = 'The data was saved'
				w.add_message('success', msg)
				
				w.category_view._categories_list(function(categories)
				{
					data.categories = categories					
					ko.mapping.fromJS(data, w.category_view.model)
					
					// for some reason i've to force this value to change
					// the select the new option on the dropdown
					// this also end up adding a new request
					w.category_view.load(data.id)
				})
			},
			error: function()
			{
				msg = 'Shit!, something is broken. Nothing was saved :(';
				w.add_message('warning', msg)
			}
		}

		// convert the view model into a js object
		data = ko.toJS(w.category_view.model);
		
		id = data.id
		
		// remove knockout keys
		delete data.__ko_mapping__;		
		data = JSON.stringify(data);
		w.clear_errors();

		// send the data to the endpoint
		if(id > 0)
		{			
			w.ajax('/api/v1/category/'+id, 'PUT', data, callback)
		}
		else
		{
			w.ajax('/api/v1/category/', 'POST', data, callback)
		}
	},
	/**
	 * Show the delete alert
	 */
	del: function()
	{
		w.clear_errors();
		var category_name = $('#category option:selected').text();

		// create the alert dialog object
		var alert = new w.alert.create();
		alert.ok_label = 'Yes, delete it';
		alert.cancel_label = 'No, don\'t delete it!!';
		alert.head_text = 'Watch out!!';
		alert.body_text = 'Are you sure you want to delete the category <strong>'+category_name+'</strong> ?';
		alert.ok_function = 'w.category_view._del()';
		alert.show();
	},
	/**
	 * Delete the category
	 */
	_del: function()
	{
		var callback =
		{
			success: function(data, textStatus)
			{
				msg = 'The category was deleted'
				w.add_message('success', msg)
				$('#category').find('option[value="'+id+'"]').remove()
				$('#category_form')[0].reset(); 
				
				w.category_view.load($('#category option').first().val())				
			},
			error: function()
			{
				msg = 'Shit!, something is broken. Nothing was deleted :(';
				w.add_message('warning', msg)
			}
		}

		id = w.category_view.model.id()

		// call the endpoint to delete the category
		w.ajax('/api/v1/category/'+id, 'DELETE', {}, callback)
	}
}

/**
 * History row object
 * @param  {object} item        
 * @param  {object} wallet      
 * @param  {object} transaction 
 */
function history_view_row(item, wallet, transaction)
{
	var self = this;
	self.item = item;
	self.wallet = wallet;
	self.transaction = transaction;
}
/**
 * History View
 */
w.history_view =
{
	rows: new Array(),
	/**
	 * Initializate the view
	 * @return {[type]} [description]
	 */
	init: function()
	{		
		w.history_view.rows = ko.observableArray([]);
		ko.applyBindings(w.history_view);
		
		w.history_view.load(1);
	},
	/**
	 * Load the records
	 * @param  {integer} page Page to be load
	 */
	load: function(page)
	{
		// get the records	
		$.getJSON("/api/v1/transactions?page="+page+'&page_size='+w.history_view.page_size, function(data)
		{
			// crate an array of rows object			
	        var mapped_row = $.map(data.results, function(v) 
	        {
	        	v.item.amount = w.format_number(v.item.amount)        	
	        	return new history_view_row(v.item, v.wallet, {'date': v.date, 'id': v.id});
	        });
	        
	        w.history_view.rows(mapped_row);
	        w.history_view.result_count = data.count;
	        
	        // load it if need it!
	        if($('#paginator').html().length <= 0 && data.count > w.history_view.page_size)
	        {
	        	w.history_view.paginator();	        	
	        }
	    });

		// TODO only call it on new search
	    if(!$('#total').html().length)
	    {
	    	w.history_view.set_total()
	    }
	},
	/**
	 * Get the history amount totals
	 */
	set_total: function()
	{
		$.getJSON("/api/v1/transactions-total", function(data)
		{
			if(data.total > 0)
			{
				$('#total').parent().addClass('text-info')
			}
			else
			{
				$('#total').parent().addClass('text-danger')
			}

			var total = w.format_number(data.total, true);
			$('#total').html(total);
		});
	},
	result_count: 0,
	page_size: 50,
	/**
	 * Creates the paginator
	 */
	paginator: function()
	{
		$('#paginator').pagination({
	        items: w.history_view.result_count,
	        itemsOnPage: w.history_view.page_size,
	        cssStyle: 'light-theme',
	        onPageClick: function(pageNumber, event)
	        {
	        	w.history_view.load(pageNumber)
	        }	        
	    });	    
	},
	/**
	 * Show the delete dialog
	 */
	del: function(data)
	{
		w.clear_errors();

		// create the alert dialog object		
		var alert = new w.alert.create();
		alert.ok_label = 'Yes, delete it';
		alert.cancel_label = 'No, don\'t delete it!!';
		alert.head_text = 'Watch out!!';
		alert.body_text = 'Are you sure you want to delete this item ?';
		alert.ok_function = 'w.history_view._del('+data.transaction.id+')';
		alert.show();
	},
	/**
	 * Delete the transaction	
	 */
	_del: function(id)
	{
		var callback =
		{
			success: function(data, textStatus)
			{
				msg = 'The item was deleted'
				w.add_message('success', msg)
				w.history_view.set_total()				
			},
			error: function()
			{
				msg = 'Shit!, something is broken. Nothing was deleted :(';
				w.add_message('warning', msg)
			}
		}

		// call the endpoint to delete the transaction
		w.ajax('/api/v1/transactions/'+id, 'DELETE', {}, callback)
	}
}

/**
 * Wallets total object
 * @param  {object} wallet
 * @param  {object} total
 */
function dashboard_view_wallet_widget_row(wallet, total)
{
	var self = this;
	self.wallet = wallet;
	self.total = total;
}

/**
 * Dashboard view
 */
w.dashboard_view =
{
	wallets_rows: {},
	/**
	 * Initializate the view
	 */
	init: function()
	{
		w.dashboard_view.wallets_rows = ko.observableArray([]);
		ko.applyBindings(w.dashboard_view);

		// Get the wallet's total
		$.getJSON("/api/v1/wallet-total/", function(data)
		{
			// create the wallet total objects
	        var mapped_wallet = $.map(data.results, function(v) 
	        {
	        	var total = Number(v.wallet.initial_amount) + Number(v.total)
	        	total = w.format_number(total);

	        	return new dashboard_view_wallet_widget_row(v.wallet, total) 
	        });

	        w.dashboard_view.wallets_rows(mapped_wallet);
	    });	    
	},
	/**
	 * Logout the user
	 */
	logout: function()
	{
		var callback =
		{
			success: function(data, textStatus)
			{
				window.location.replace('/')
			}
		}		

		w.ajax('/api/v1/auth/logout/', 'POST', null, callback)
	}
}

/**
 * Home View
 */
w.home_view =
{
	/**
	 * Validate and login the user
	 */
	login: function()
	{
		var callback =
		{
			success: function(data, textStatus)
			{				
				window.location.replace('/dashboard');
			},
			error: function()
			{
				$('#login_result').hide().fadeIn('fast');
				$('#btn_login').button('reset');
			}
		}

		data = {
			'username': $('#username').val(),
			'password': $('#password').val(),
			'csrf': $('input[name="csrf"]').val()
		}

		w.ajax('/api/v1/auth/login/', 'POST', JSON.stringify(data), callback)
	},
	/**
	 * Initializate the view
	 */
	init: function()
	{
		// button bindings
		$('#form_signin').submit(function(e){ 
			w.home_view.login();
			$('#btn_login').button('loading');
			 event.preventDefault();
		});

		$('#btn_register').click(function(){
	      $('#signin').slideUp('fast', function(){
	        $('#register').slideDown('fast')
	      });
	    });

	    $('.btn_back_login').click(function(){
	      $('#register, #reset_pass').slideUp('fast', function(){
	        $('#signin').slideDown('fast')
	      });
	    });

	    $('#btn_reset_pass').click(function(){
	      $('#signin').slideUp('fast', function(){
	        $('#reset_pass').slideDown('fast')
	      });
	    });

	    $('#link_what_is_it').click(function() { $('#what_is_it').slideToggle() });
	}
}