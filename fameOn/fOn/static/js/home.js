<script type = "text/javascript">
//Show all the posts on the page load
$(document).ready(function(){
	alert('hi');
	current_obj = $(this);
	$.ajax({
		type:"GET",
		url:"/fOn/show_posts/",
		data:{},
		success: function(json){
		$.each(json.post, function(key, value){

			html_str = '<div class = "mycolor postpanel shadow" data-postdel="'+value.id+'">\
				<div  class = "post heading">\
					<div>\
						<h4 class="profile-name likeunlike">Post</h4>\
						<button class="delpost pull-right" data-delid="'+value.id+'">\
						<span class="glyphicon glyphicon-remove"></span>\
						</button>\
					</div>\
					<div class="title h5">\
						<h5 class="profile-name">'+value.user_posted+'</h5>\
					</div>\
					<h6 class="text-muted-time">'+value.created+'</h6>\
				</div>\
				<div calss="post-description">\
					<h5 class="mycolor">Post :'+value.body+'</h5>\
					<div class="stats">\
						<button id="likes'+value.id+'" class="likebutton" data-catid="'+value.id+'" type="button" href="#">\
							<span class="glyphicon glyphicon-thumbs-up"></span>\
						</button>\
						<p class="like likeunlike">'+value.like+'</p>\
						<button id="unlike'+value.id+'" class="unlikebutton likeunlike" data-catid="'+value.id+'" type="button" href="#">\
							<span class="glyphicon glyphicon-thumbs-down"></span>\
						</button>\
					</div>\
				</div>\
				<div class="post-footer">\
						<div class = "add-comment-first">\
						<button class="display-comment" id= "display-commentid" data-dcomment='+value.id+'><h5 class="profile-name" type="submit">Comments</h5></button>\
						</div>\
				</div>';
			$('div.display-post').append(html_str);
			});
		}
	});
});

//create a post
$('#postformid').on('submit', function(event){
	event.preventDefault();
	create_post();
});

function create_post() {
	$.ajax({
		url : "/fOn/create_post/",
		type : "POST",
		data : {'post' : $('#post-text').val(),},
		success : function(response){
			$('#post-text').val('');
			html_str = 			'<div class = "mycolor postpanel shadow" data-postdel="'+response.post_id+'">\
				<div  class = "post heading">\
					<div>\
						<h4 class="profile-name likeunlike">Post</h4>\
						<button class="delpost pull-right" data-delid="'+response.post_id+'">\
							<span class="glyphicon glyphicon-remove"></span>\
						</button>\
					</div>\
					<div class="title h5">\
						<h5 class="profile-name">'+response.author+'</h5>\
					</div>\
				  <h6 class="text-muted-time">'+response.publish+'</h6>\
				</div>\
				<div calss="post-description">\
					<h5 class="mycolor">Post : '+response.post+'</h5>\
					<div class="stats">\
						<button id="likes'+response.post_id+'" class="likebutton" data-catid="'+response.post_id+'" type="button" href="#">\
							<span class="glyphicon glyphicon-thumbs-up"></span>\
						</button>\
						<p class="like likeunlike"></p>\
						<button id="unlike'+response.post_id+'" class="unlikebutton likeunlike" data-catid="'+response.post_id+'" type="button" href="#">\
							<span class="glyphicon glyphicon-thumbs-down"></span>\
						</button>';
					
				html_str +=	'</div>\
					 <div class="post-footer">\
							<div class = "add-comment-first">\
								<button class="display-comment" id= "display-commentid" data-dcomment='+response.post_id+' type="submit"><h5 class="profile-name">Comments</h5>\
								</button>\
							</div>\
					</div>\
			</div>';

			$('div.newpost').append(html_str);
		},
	});
};



//shows all the comments and input box
$(document).on('click','.display-comment', function(){
	var catid;
	current_obj = $(this);
	catid = $(this).attr('data-dcomment');
	$.ajax({
		url: "/fOn/show_comments/",
		type: "POST",
		data: {post_id:catid,},
		success: function(response){
			current_obj.parent('.add-comment-first').append('\
					<div>\
						<p>\
						<input class="form-control add-comment-input" placeholder="Add a comment..." type="text" required=""></p>\
						<div class="latest-comment-on">\
							<button class="comment_submit btn btn-primary" type="submit" data-postid='+response.post_id+'>Submit</button>\
						</div>\
					</div>');
			$.each(response.comment, function(key, value){
				current_obj.parents('div.post-footer').append('\
				<div>\
					<li class="comment">\
						<div>\
							<button class="delcomment pull-right" data-delid="'+value.comment_id+'">\
								<span class="glyphicon glyphicon-remove"></span>\
							</button>\
						</div>\
						<a class="pull-left likeunlike" href="#">\
							<img class="avtar" src =""></img>\
						</a>\
						<div class="comment-heading likeunlike">\
							<h5 class="comment-user-name profile-name likeunlike">'+value.user_commented+'<a href="#"></a><h6 class="likeunlike">: commented on, </h6>\
							</h5>\
							<h5 class="time likeunlike">'+value.created_date+'</h5>\
							<p>'+value.text+'</p>\
						</div>\
					</li>\
				</div>');
			});
		}
	});
})

//create a comment
$(document).on('click', '.comment_submit', function(){
	current_obj = $(this);
	var catid;
	catid = $(this).attr('data-postid');
	var value=$.trim($(".add-comment-input").val());
	if (value.length>0){
		$('#display-commentid').hide();
		execute_further();
	}
	function execute_further(){
		$.ajax({
			type:"POST",
			url:'/fOn/comment/',
			data:{comment: $('.add-comment-input').val(), post: catid,},
			success: function(response){
				$('.add-comment-input').val('');
				current_obj.parent('.latest-comment-on').append(
					'<li class="comment" id='+response.comment_id+'>\
						<div>\
							<button class="delcomment pull-right" data-delid="'+response.comment_id+'">\
								<span class="glyphicon glyphicon-remove"></span>\
							</button>\
						</div>\
						<a class="pull-left likeunlike" href="#">\
							<img class="avtar" src =""></img>\
						</a>\
						<div class="comment-heading likeunlike">\
							<h5 class="comment-user-name profile-name likeunlike">'+response.usercomment+'<a href="#"></a><h6 class="likeunlike">: commented on, </h6>\
							</h5>\
							<h5 class="time likeunlike">'+response.comment_date+'</h5>\
							<p>'+response.comment_text+'</p>\
						</div>\
					</li>');
			}
		});
	}

});

//Unlike on post
$(document).on('click', '.likebutton', function(){
	var catid;
	current_obj = $(this);
	catid = $(this).attr("data-catid");
	$.ajax({
		type:"GET",
		url: '/fOn/likepost/',
		data:{ post_id: catid },
		success: function(response){
			// $('#likes'+ catid).remove();
			current_obj.parent().find('p.like').text(response.likes_count)
		}
	})
});

// Like on post
$(document).on('click', '.unlikebutton', function(){
	var catid;
	current_obj = $(this);
	catid = $(this).attr("data-catid");
		$.ajax({
			type:"GET",
			url:'/fOn/unlikepost/',
			data:{ post_id: catid },
			success: function(response){
				// $('unlikes'+ catid).remove();
				current_obj.parent().find('p.like').text(response.likes_count)
			}
		})
});

//Delete a post
$(document).on('click', '.delpost', function(){
	var catid;
	current_obj = $(this);
	catid = $(this).attr("data-delid");
		$.ajax(
		  {
			type:"GET",
			url:"/fOn/delete_post/",
			data:{ post_id: catid },
			success: function(response) {
				current_obj.parents('.mycolor').fadeOut();
			},
			error: function(response) {
				alert("Couldn't remove item");
			}
		})
});

//Delete a comment
$(document).on('click', '.delcomment', function(e){
	delid = $(this).attr('data-delid');
	current_obj = $(this);
	$.ajax({
		type:"GET",
		url:"/fOn/delete_comment/",
		data:{comment_id: delid,},
		success: function(response){
		current_obj.parents('.comment').fadeOut();        
		},
		error: function(e){
			alert("Couldn't remove the comment");
		}
	});
});

//Search bar
$(document).ready(function(){
	$("input#srch-term").keyup(function(){
		var query = $(this).val();
		if(query.length>2){
			$.ajax({
				type: "POST",
				url: "/fOn/get_user_detail/",
				data: {'search_text': $('#srch-term').val(),},
				success: searchSuccess,
				dataType:'html'
			});
		}
	});
	$("#srch-term").val('');
});

function searchSuccess(data, textStatus, jqXHR)
{
	$('#search-results-id').html(data);
}

$(document).ready(function(){
	$("input[type='file']").change(function(){
        readURL(this);
    });
    function readURL(input) {
        $("#prof-image").submit();
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('.img-responsive').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    $('form').ajaxForm({
            url:"/fOn/upload_image/",
            type: 'POST',
            dataType: 'json',
            clearForm: false,
            resetForm: false,
             
            success: function(result) {
                
            },
            error: function(result){
                
            },
        });
});

//image submit through modelform

// $('#form1').on('submit', function(e) {
//     e.preventDefault();
//     // data = new FormData($('form').get(0));
//     if (this.files && this.files[0]) {
//           var reader = new FileReader();
//           reader.onload = function (e) {
//               $('.img-responsive').attr('src', e.target.result);
//           }
          
//     reader.readAsDataURL(this.files[0]);
// 	}
//     alert(' hi');
//     $.ajax({
//        	url : "/fOn/upload_image/",
//         	type: "POST",
//         	data: data,
//         	contentType:false,
//     		processData:false,
//     		cache:false,
//     		dataType:"json"
//         	success: function (data) {
//         	alert('success');
       
//         },  
//     })
// });

// image send on onchange using base64/////////////////////
// $(document).ready(function(){
// 	 $("input[type='file']").change(function(){
//        if (this.files && this.files[0]) {
//           var reader = new FileReader();
//           reader.onload = function (e) {
//               $('.img-responsive').attr('src', e.target.result);
               
//               var data = {'img' : e.target.result}
//                $.ajax({
//                    type: "POST",
//                    url: '/fOn/upload_image/',
//                    data: data,
//                    // {'img' : e.target.result},
//                    // cache: false,
//                    // processData: false,
//                    // contentType: "application/json; charset=utf-8",
//                    success: function(response){
//                        alert(response.message);
//                    },
//                    error: function(rs, e){
//                        alert("Error");

//                },
//            });
//           }
//           reader.readAsDataURL(this.files[0])
//           // var form = $('form')[0];
//           // var data = new FormData(form);
//           // var formData = new FormData(this);
//        }          
//    });
// });




</script>