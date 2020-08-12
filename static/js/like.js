$('.likes-button').click(function () {
    var ansid;
    ansid = $(this).attr("data-ansid");
    $.get(`/issues/add_like/${ansid}`, function (data) {
        $(`#like_count_${ansid}`).html(data);
        $('#likes').hide();
    });
    console.log(`liked/disliked-${ansid}`)
});

function myFunction(x) {
    y = x.children[0];
    if (y.classList[1] == "fa-thumbs-up") {
        y.classList.toggle("fa-thumbs-down");
        console.log('liked')
    }
    if (y.classList[1] == "fa-thumbs-down") {
        y.classList.add("fa-thumbs-up")
        y.classList.remove("fa-thumbs-down");
        console.log('disliked')
    }
}