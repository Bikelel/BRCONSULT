$(function () {
    for (let pas = 0; pas < 20; pas++) {
        
        $('#datetimepicker_date_constat_'+pas).datetimepicker({
            format: 'L',
            locale : 'fr',
        });
        
    }

  $('#datetimepicker_scheduled_date_act').datetimepicker({
    format: 'L',
    locale : 'fr',
    });
})