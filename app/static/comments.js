$(document).ready(function() {
    $(".submit-comment").on("click", function(e) {
        e.preventDefault();
        const post_id = $(this).data("post-id");
        const commentContent = $('#comment-input-${post_id}').val();
        const csrfToken = $('meta[name="csrf-token"]').attr("content");
        if (!commentContent.trim()) {
            alert("Content should not be empty");
            return;
        }
        $.ajax({
            url: '/add_comment/${post_id}',
            type: "POST",
            contentType: "application/json",
            headers: {
                "x-CSRFToken": csrfToken,
            },
            data: JSON.stringify({
                content: commentContent,
            }),
            success: function (response) {
                const newComment = '<p><strong>${response.author}: ${response.content}</strong></p>';
                $('#comments-section-${post_id}').append(newComment);
                $('#comments-input-${post_id}').val("");
            },
            error: function(xhr) {
                alert(xhr.responseJSON.error || "Failed to submit comment");
            },
        })
    })
})