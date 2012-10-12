jQuery(document).ready(function()
		       {
			   jQuery('input:button').click(function(e)
							{
							    var bookTitle = this.id.substr(6);
							    var doDelete = confirm('Click OK to delete '+bookTitle);
							    if(doDelete)
							    {
								jQuery.post('deleteBook', data={'bookTitle': bookTitle},
									    success=function(list)
									    {
										jQuery('#bookList').html(list);
									    }, 'html');
							    }
							});
		       });