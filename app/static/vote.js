$(document).ready(function() {
	var csrf_token = $('meta[name=csrf-token]').attr('content');
	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrf_token);
	        }
	    }
	});	
	$("a.vote").on("click", function() {
		var clicked_obj = $(this);
		var post_id = $(this).attr('id');
		var vote_type = $(this).children()[0].id;
		$.ajax({
			url: '/vote',
			type: 'POST',
			data: JSON.stringify({ post_id: post_id, vote_type: vote_type}),
			contentType: "application/json; charset=utf-8",
        	dataType: "json",
			success: function(response){
				console.log(response);
				if(vote_type == "up") {
					clicked_obj.children()[1].innerHTML = " " + response.upvotes;
				} else {
					clicked_obj.children()[1].innerHTML = " " + response.downvotes;
				}
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});