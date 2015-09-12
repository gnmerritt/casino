window.makeBot = function() {
    var name = $("#botName").val();
    if (!name) return;
    $.ajax({
        url: "/api/bot/" + encodeURIComponent(name),
        type: "POST"
    }).done(function() {
        window.location.reload();
    });
};
