from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _


class RestrictedFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop('content_types', None)
        self.max_upload_size = kwargs.pop('max_upload_size', None)
        if not self.max_upload_size:
            self.max_upload_size = 20971520
        super(RestrictedFileField, self).__init__(*args, **kwargs)
 
    def clean(self, *args, **kwargs):
        cleaned_data = super(RestrictedFileField, self).clean(*args, **kwargs)
        try:
            is_in_content_types = False
            for content_type in self.content_types:
                if cleaned_data.content_type.startswith(content_type):
                    is_in_content_types = True
            if is_in_content_types:
                if cleaned_data.size > self.max_upload_size:
                    raise forms.ValidationError(_('File size must be under %s. Current file size is %s.') % (filesizeformat(self.max_upload_size), filesizeformat(cleaned_data.size)))
            else:
                raise forms.ValidationError(_('File type (%s) is not supported.') % cleaned_data.content_type)
        except AttributeError:
            pass
        return cleaned_data