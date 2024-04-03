function clickServiceLink(buttonId, hiddenSpanId, elementToToggleId) {

    // Кейс с повторно нажатой кнопкой, закрываем все что есть
    var isCurrentlyActive = $("#" + buttonId).hasClass('active');

    if(isCurrentlyActive) {
        $('.btn-service').removeClass('active');
        $("#" + elementToToggleId).hide();
    } else {

        // Toggle visibility of the element
        $("#" + elementToToggleId).show();

        // Get value from hidden input and append to the content if the element is visible
        if ($("#" + elementToToggleId).is(":visible")) {
            var hiddenIdValue = $("#" + hiddenSpanId).text(); // Get the ID value
            // Append the ID value to the href of the link inside the elementToToggle
            $("#" + elementToToggleId + " a").attr("href", function(i, originalHref) {
                return "./sandbox-services.html?service_id=" + hiddenIdValue;
            });
        }

        $('.btn-service').removeClass('active');
        $("#" + buttonId).addClass('active');
    }
}

function clickProjectLink(buttonId, hiddenSpanId, elementToToggleId) {
    // Кейс с повторно нажатой кнопкой, закрываем все что есть
    var isCurrentlyActive = $("#" + buttonId).hasClass('active');

    if(isCurrentlyActive) {
        $('.btn-project').removeClass('active');
        $("#" + elementToToggleId).hide();
    } else {
        $('.btn-project').removeClass('active');
        $("#" + buttonId).addClass('active');
    }
}