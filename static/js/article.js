    // 点击评论按钮
$("#btn_comment_submit").click(function () {
    $.ajax({
        url:"/blog/comment/",
        type:"POST",
        data:{
            csrfmiddlewaretoken:$("[name=csrfmiddlewaretoken]").val(),
            comment:$(".comment_textarea").val(),
            comentuser:$(".varinfo").attr("commetuser"),
            article_id: $(".varinfo").attr("article_id"),
        },
        success:function (data) {
            // var data=JSON.parse(data)
            var data=data ;
            console.log(data+typeof(data)+data["create_time"]+data.create_time)

            var username=$(".varinfo").attr("username")
            var nick_name=$(".varinfo").attr("nick_name")
            var content=$("#tbCommentBody").val()
            var create_time=data['create_time']

            console.log(create_time)

            var s='<div class="feedbackItem"><div class="commenttitile"><a>#'+forloop.counter+'楼 &nbsp;</a>'
                +create_time+' &nbsp;<a href="/blog/'+username+'"' +
                '>'+nick_name+'</a><a class="pull-right" id="reply">回复</a> </div><div class="oneCommentBody">' +
                '<div>'+content+'</div></div></div>'

            console.log(s)
            $(".commentList").append(s)
            $(".comment_textarea").val("")
        }
    })

})

// 回复   事件委托，不用一个个for循环加事件，消耗内存，增加程序处理的个数  点击回复跳转到评论输入框
$(".feedbackItem").on("click","#reply",function () {
    $("#tbCommentBody").focus()
})

