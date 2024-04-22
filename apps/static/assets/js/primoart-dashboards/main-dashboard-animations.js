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
                let return_value = "./mvp-services.html?service_id=" + hiddenIdValue;
                // try to extract start_date, start_time, end_date, end_time from the originalHref and append if 4 values are found
                let url = new URL(window.location.href);
                let start_date = url.searchParams.get("start_date");
                let start_time = url.searchParams.get("start_time");
                let end_date = url.searchParams.get("finish_date");
                let end_time = url.searchParams.get("finish_time");
                if (start_date && start_time && end_date && end_time) {
                    return_value += "&start_date=" + start_date + "&start_time=" + start_time + "&finish_date=" + end_date + "&finish_time=" + end_time;
                }

                return return_value;
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
                let return_value = "./mvp-robots.html?robot_id=" + hiddenIdValue;

                // try to extract start_date, start_time, end_date, end_time from the originalHref and append if 4 values are found
                let url = new URL(window.location.href);
                let start_date = url.searchParams.get("start_date");
                let start_time = url.searchParams.get("start_time");
                let end_date = url.searchParams.get("finish_date");
                let end_time = url.searchParams.get("finish_time");
                if (start_date && start_time && end_date && end_time) {
                    return_value += "&start_date=" + start_date + "&start_time=" + start_time + "&finish_date=" + end_date + "&finish_time=" + end_time;
                }

                return return_value;

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
                let return_value = "./mvp-transaction.html?transaction_id=" + hiddenIdValue;

                // try to extract start_date, start_time, end_date, end_time from the originalHref and append if 4 values are found
                let url = new URL(window.location.href);
                let start_date = url.searchParams.get("start_date");
                let start_time = url.searchParams.get("start_time");
                let end_date = url.searchParams.get("finish_date");
                let end_time = url.searchParams.get("finish_time");
                if (start_date && start_time && end_date && end_time) {
                    return_value += "&start_date=" + start_date + "&start_time=" + start_time + "&finish_date=" + end_date + "&finish_time=" + end_time;
                }

                return return_value;

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
                let return_value = "./mvp-main-dashboard.html?project_id=" + hiddenIdValue;

                // try to extract start_date, start_time, end_date, end_time from the originalHref and append if 4 values are found
                let url = new URL(window.location.href);
                let start_date = url.searchParams.get("start_date");
                let start_time = url.searchParams.get("start_time");
                let end_date = url.searchParams.get("finish_date");
                let end_time = url.searchParams.get("finish_time");
                if (start_date && start_time && end_date && end_time) {
                    return_value += "&start_date=" + start_date + "&start_time=" + start_time + "&finish_date=" + end_date + "&finish_time=" + end_time;
                }

                return return_value;
            });
        }

        $('.btn-project').removeClass('active');
        $("#" + buttonId).addClass('active');
    }
}