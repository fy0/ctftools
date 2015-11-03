(function($) {
    'use strict';

    $(function() {
        var file_items = [
        ];

        var demo = new Vue({
            el: '#upload-box',
            data: {
                file_items: file_items,
            },
        })

        $.post("/j/upload_file_lst", function(ret) {
            for (var i in ret) {
                var item = ret[i];
                file_items.push(item);
            }
        });

        $('#doc-form-file').on('change', function() {
            var fileNames = '';
            $.each(this.files, function() {
                fileNames += '<span class="am-badge">' + this.name + '</span> ';
            });
            $('#file-list').html(fileNames);
        });

        $('#file_upload').dmUploader({
            url: '/j/upload',
            dataType: 'json',
            onInit: function(){
            },
            onBeforeUpload: function(id){
            },
            onNewFile: function(id, file){
                console.log('New file added to queue #' + id);
                //add_file(id, file);
            },
            onComplete: function(){
            },
            onUploadProgress: function(id, percent){
            },
            onUploadSuccess: function(id, data){
                console.log('Upload of file #' + id + ' completed');
                console.log('Server Response for file #' + id + ': ' + JSON.stringify(data));
                //update_file_status(id, 'success', 'Upload Complete');
                //update_file_progress(id, '100%');
                file_items.push(data);
            },
            onUploadError: function(id, message){
                console.log('Failed to Upload file #' + id + ': ' + message);
                //update_file_status(id, 'error', message);
            },
            onFileTypeError: function(file){
                console.log('File \'' + file.name + '\' cannot be added: must be an image');
            },
            onFileSizeError: function(file){
                console.log('File \'' + file.name + '\' cannot be added: size excess limit');
            },
            onFallbackMode: function(message){
                alert('Browser not supported(do something else here!): ' + message);
            }
        });

    });
})(jQuery);
