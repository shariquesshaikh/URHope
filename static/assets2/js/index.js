$(document).ready(function () {
    $("select.filter").change(function () {
        var selectedOption = $(this).children("option:selected").val();
        if (selectedOption === 'Choose Filter...') {
            var value = '';
            $("table tbody > tr ").filter(function () {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
            });
        } else {
            var value = selectedOption.toLowerCase();
            $("table tbody > tr ").filter(function () {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
            });
        }
    });
});


$(document).ready(function () {
    $('.filter-import').load('filter.html');
});
$(document).ready(function () {
    $('.master-import').load('old_index.html');
});
