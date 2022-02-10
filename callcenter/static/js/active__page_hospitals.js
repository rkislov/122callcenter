    var current_page = 1; // maintains the current page
    var page_limit = 10; // the limit of results shown on page.
    var sort_by = ""; // maintains the select option for sort_by
    var active = ""; // maintains the select option for country
    var start = ""; // maintains the select option for start_yr
    var end = ""; // maintains the select option for end_yr
    var hospital = "";

    function get_list_url(page) {
        // returns the consructed url with query params.
        return `/hospital/api/get/calls_hospital?page=${page}&limit=${page_limit}&active=${active}&sort_by=${sort_by}&start=${start}&end=${end}&hospita=${hospital}`;
    }

    function getCallResult() {
        // call the ajax and populates the country select options
        $.ajax({
            method: 'GET',
            url: $("#call_result").attr("url"),
            success: function (response) {
                call_result_option = "<option value='true' selected>Результат</option>";
                $.each(response["call_result"], function (a, b) {
                    call_result_option += "<option>" + b + "</option>"
                });
                $("#call_result").html(call_result_option)
                $('select').formSelect();
            },
            error: function (response) {
                console.log(response)
            }
        });
    }

    // On select change of the country select, call the getAPIData
    $("#countries").on("change", function (e) {
        current_page = 1;
        country = this.value
        getAPIData(get_list_url(current_page));
    });
    // On select change of the year select, call the getAPIData
    $("#start").on("change", function (e) {
        current_page = 1;
        start = $(this).val();
        getAPIData(get_list_url(current_page));
    })
    $("#end").on("change", function (e) {
        current_page = 1;
        end = $(this).val();
        getAPIData(get_list_url(current_page));
    })
    // On select change of the sort select, call the getAPIData with sortby.
    $("#sort").on("change", function (e) {
        current_page = 1;
        sort_by = this.value
        getAPIData(get_list_url(current_page));
    })
    $("#page_limit").on("change", function (e) {
        current_page = 1;
        page_limit = this.value
        getAPIData(get_list_url(current_page));
    })
// Helper method that popluates the html table with next and prev
    // url, and current page number.
    function putTableData(response) {
        // creating table row for each response and
        // pushing to the html cntent of table body of table_body table
        let row;
        $("#table_body").html("");
        if (response["data"].length > 0) {
            $.each(response["data"], function (a, b) {
                row = "<tr> <td>" + b.date + "</td>" +
                    "<td>" + b.call_number + "</td>" +
                    "<td>" + b.active + "</td>" +
                    $("#table_body").append(row);
            });
        }
        else{
            // if there is no results found!
           $("#table_body").html("Нет записей"); 
        }
        if (response.pagination.has_prev) {
            // sets the previous page url.
            $("#previous").attr("data-url", get_list_url(current_page - 1));
            $("#previous").attr("disabled", false);
        } else {
            // if there is no prev page available, disable the btn.
            $("#previous").attr("disabled", true);
        }
        if (response.pagination.has_next) {
            // sets the next page url.
            $("#next").attr("data-url", get_list_url(current_page + 1));
            $("#next").attr("disabled", false);
        } else {
            // if there is no next page available, disable the btn.
            $("#next").attr("disabled", true)
        }
    }

    // On click of next/prev button, call the getAPIData with the given url.
    $(".page-link").click(function (e) {
        e.preventDefault();
        let url = $(this).attr("data-url");
        getAPIData(url);
    })

    // Main method which calls AJAX to get the data from backend.
    function getAPIData(url) {
        $.ajax({
            method: 'GET',
            url: url,
            success: function (response) {
                current_page = parseInt(response.pagination.page)
                putTableData(response);
                // put the total result count.
                $("#result-count span").html(response.pagination.total)
                $("#page-count span").html(response.pagination.page)
            },
            error: function (response) {
                $("#hero_table").hide();
            }
        });
    }

    getAPIData(get_list_url(current_page));
    getCallResult()