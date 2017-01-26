
// dirty fix for make uploader working in django admin inline
django.jQuery(function($){
    var container = $('#content-main').delegate('.add-row', 'click', function(e){
        container.find('.ajax-upload-mark').each(function(i, el){
            var uploader_input = $(el);
            if(uploader_input.attr('name').lastIndexOf('__prefix__') == -1){
                uploader_input.removeClass('ajax-upload-mark');
                new AjaxUploadWidget(uploader_input, uploader_input.data('uploader_options') || {});
            }
        });
    });
});