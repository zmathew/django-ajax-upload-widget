(function() {
    var global = this;
    var $ = global.$;
    var console = global.console || {log: function() {}};

    var AjaxUploadWidget = global.AjaxUploadWidget = function(element, options) {
        this.options = {
            changeButtonText: 'Change',
            removeButtonText: 'Remove',
            previewAreaClass: 'ajax-upload-preview-area',
            previewFilenameLength: 30,
            onUpload: null, // right before uploading to the server
            onComplete: null,
            onError: null,
            onRemove: null
        };
        $.extend(this.options, options);
        this.$element = $(element);
        this.initialize();
    };

    AjaxUploadWidget.prototype.DjangoAjaxUploadError = function(message) {
        this.name = 'DjangoAjaxUploadError';
        this.message = message;
    };
    AjaxUploadWidget.prototype.DjangoAjaxUploadError.prototype = new Error();
    AjaxUploadWidget.prototype.DjangoAjaxUploadError.prototype.constructor = AjaxUploadWidget.prototype.DjangoAjaxUploadError;

    AjaxUploadWidget.prototype.initialize = function() {
        var self = this;
        this.name = this.$element.attr('name');

        // Create a hidden field to contain our uploaded file name
        this.$hiddenElement = $('<input type="hidden"/>')
            .attr('name', this.name)
            .val(this.$element.data('filename'));
        this.$element.attr('name', ''); // because we don't want to conflict with our hidden field
        this.$element.after(this.$hiddenElement);

        // Initialize preview area and action buttons
        this.$previewArea = $('<div class="'+this.options.previewAreaClass+'"></div>');
        this.$element.before(this.$previewArea);

        // Listen for when a file is selected, and perform upload
        this.$element.on('change', function(evt) {
            self.upload();
        });
        this.$changeButton = $('<button type="button" class="btn-change"></button>')
            .text(this.options.changeButtonText)
            .on('click', function(evt) {
                self.$element.show();
                $(this).hide();
            });
        this.$element.after(this.$changeButton);

        this.$removeButton = $('<button type="button" class="btn-remove"></button>')
            .text(this.options.removeButtonText)
            .on('click', function(evt) {
                if(self.options.onRemove) {
                    var result = self.options.onRemove.call(self);
                    if(result === false) return;
                }
                self.$hiddenElement.val('');
                self.displaySelection();
            });
        this.$changeButton.after(this.$removeButton);

        this.displaySelection();
    };

    AjaxUploadWidget.prototype.upload = function() {
        var self = this;
        if(!this.$element.val()) return;
        if(this.options.onUpload) {
            var result = this.options.onUpload.call(this);
            if(result === false) return;
        }
        this.$element.attr('name', 'file');
        $.ajax(this.$element.data('upload-url'), {
            iframe: true,
            files: this.$element,
            processData: false,
            type: 'POST',
            dataType: 'json',
            success: function(data) { self.uploadDone(data); },
            error: function(data) { self.uploadFail(data); }
        });
    };

    AjaxUploadWidget.prototype.uploadDone = function(data) {
        // This handles errors as well because iframe transport does not
        // distinguish between 200 response and other errors
        if(data.errors) {
            if(this.options.onError) {
                this.options.onError.call(this, data);
            } else {
                console.log('Upload failed:');
                console.log(data);
            }
        } else {
            this.$hiddenElement.val(data.path);
            var tmp = this.$element;
            this.$element = this.$element.clone(true).val('');
            tmp.replaceWith(this.$element);
            this.displaySelection();
            if(this.options.onComplete) this.options.onComplete.call(this, data.path);
        }
    };

    AjaxUploadWidget.prototype.uploadFail = function(xhr) {
        if(this.options.onError) {
            this.options.onError.call(this);
        } else {
            console.log('Upload failed:');
            console.log(xhr);
        }
    };

    AjaxUploadWidget.prototype.displaySelection = function() {
        var filename = this.$hiddenElement.val();

        if(filename !== '') {
            this.$previewArea.empty();
            this.$previewArea.append(this.generateFilePreview(filename));

            this.$previewArea.show();
            this.$changeButton.show();
            if(this.$element.data('required') === 'True') {
                this.$removeButton.hide();
            } else {
                this.$removeButton.show();
            }
            this.$element.hide();
        } else {
            this.$previewArea.slideUp();
            this.$changeButton.hide();
            this.$removeButton.hide();
            this.$element.show();
        }
    };

    AjaxUploadWidget.prototype.generateFilePreview = function(filename) {
        // Returns the html output for displaying the given uploaded filename to the user.
        var prettyFilename = this.prettifyFilename(filename);
        var output = '<a href="'+filename+'" target="_blank">'+prettyFilename+'';
        $.each(['jpg', 'jpeg', 'png', 'gif'], function(i, ext) {
            if(filename.toLowerCase().slice(-ext.length) == ext) {
                output += '<img src="'+filename+'"/>';
                return false;
            }
        });
        output += '</a>';
        return output;
    };

    AjaxUploadWidget.prototype.prettifyFilename = function(filename) {
        // Get rid of the folder names
        var cleaned = filename.slice(filename.lastIndexOf('/')+1);

        // Strip the random hex in the filename inserted by the backend (if present)
        var re = /^[a-f0-9]{32}\-/i;
        cleaned = cleaned.replace(re, '');

        // Truncate the filename
        var maxChars = this.options.previewFilenameLength;
        var elipsis = '...';
        if(cleaned.length > maxChars) {
            cleaned = elipsis + cleaned.slice((-1 * maxChars) + elipsis.length);
        }
        return cleaned;
    };

    AjaxUploadWidget.autoDiscover = function(options) {
        $('input[type="file"].ajax-upload').each(function(index, element) {
            new AjaxUploadWidget(element, options);
        });
    };
}).call(this);
