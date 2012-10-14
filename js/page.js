jQuery(document).ready(function()
		       {
			   jQuery('#page_body_edit').hide();
			   jQuery('#editSwitch').click(function(e)
						       {
							   e.preventDefault();
							   jQuery('#page_body_edit').show();
							   jQuery('#page_body').hide();
						       });
			   jQuery('#cancelEdit').click(function(e)
						       {
							   e.preventDefault();
							   jQuery('#page_body_edit').hide();
							   jQuery('#page_body').show();
						       });
			   jQuery('input:button').click(function(e)
							{
							    var parts = this.id.substr(6).split('_');
							    var title = parts[0];
							    var page_name = parts[1];
							    jQuery.ajax({
								type: 'DELETE', 
								url: '/book/'+title+'/'+page_name,
								success: function(list)
								{
								    jQuery('#page_list').html(list);
								},
								dataType: 'html'
							    });
							});
		       });