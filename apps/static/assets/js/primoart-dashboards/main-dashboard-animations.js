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
                //console.log("[DBG][clickServiceLink] originalHref=" + originalHref);

                // TODO: Реализовать создание валидных ссылок для sandbox и mvp
                return "./mvp-services.html?service_id=" + hiddenIdValue;
                //return originalHref + "?service_id=" + hiddenIdValue;
            });
        }

        $('.btn-service').removeClass('active');
        $("#" + buttonId).addClass('active');
    }
}

function clickRobotLink(buttonId, hiddenSpanId, elementToToggleId) {

    // Кейс с повторно нажатой кнопкой, закрываем все что есть
    var isCurrentlyActive = $("#" + buttonId).hasClass('active');

    if(isCurrentlyActive) {
        $('.btn-robot').removeClass('active');
        $("#" + elementToToggleId).hide();
    } else {

        // Toggle visibility of the element
        $("#" + elementToToggleId).show();

        // Get value from hidden input and append to the content if the element is visible
        if ($("#" + elementToToggleId).is(":visible")) {
            var hiddenIdValue = $("#" + hiddenSpanId).text(); // Get the ID value
            // Append the ID value to the href of the link inside the elementToToggle
            $("#" + elementToToggleId + " a").attr("href", function(i, originalHref) {
                return "./mvp-robots.html?robot_id=" + hiddenIdValue;

                // TODO: Реализовать создание валидных ссылок для sandbox и mvp
                //return originalHref + "?robot_id=" + hiddenIdValue;
            });
        }

        $('.btn-robot').removeClass('active');
        $("#" + buttonId).addClass('active');
    }
}

function clickTransactionLink(buttonId, hiddenSpanId, elementToToggleId) {

    // Кейс с повторно нажатой кнопкой, закрываем все что есть
    var isCurrentlyActive = $("#" + buttonId).hasClass('active');

    if(isCurrentlyActive) {
        $('.btn-transaction').removeClass('active');
        $("#" + elementToToggleId).hide();
    } else {

        // Toggle visibility of the element
        $("#" + elementToToggleId).show();

        // Get value from hidden input and append to the content if the element is visible
        if ($("#" + elementToToggleId).is(":visible")) {
            var hiddenIdValue = $("#" + hiddenSpanId).text(); // Get the ID value
            // Append the ID value to the href of the link inside the elementToToggle
            $("#" + elementToToggleId + " a").attr("href", function(i, originalHref) {
                return "./mvp-transaction.html?transaction_id=" + hiddenIdValue;

                // TODO: Реализовать создание валидных ссылок для sandbox и mvp
                //return originalHref + "?robot_id=" + hiddenIdValue;
            });
        }

        $('.btn-transaction').removeClass('active');
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

        // Toggle visibility of the element
        $("#" + elementToToggleId).show();

        // Get value from hidden input and append to the content if the element is visible
        if ($("#" + elementToToggleId).is(":visible")) {
            var hiddenIdValue = $("#" + hiddenSpanId).text(); // Get the ID value
            // Append the ID value to the href of the link inside the elementToToggle
            $("#" + elementToToggleId + " a").attr("href", function (i, originalHref) {
                return "./mvp-main-dashboard.html?project_id=" + hiddenIdValue;
            });
        }

        $('.btn-project').removeClass('active');
        $("#" + buttonId).addClass('active');
    }
}