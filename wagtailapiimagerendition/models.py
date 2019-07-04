"""
.. module:: wagtailapiimagerendition.models
"""


class WithApiRenditionMixin(object):
    @property
    def link(self):
        """ link """
        if self.file:
            return self.file.url
        else:
            return ''

    def generate_and_get_rendition(self, rendition_size):
        """ generate_and_get_rendition """
        if not self.file or rendition_size == 'none':
            return self.file.url
        else:
            return self.get_rendition('fill-{}'.format(rendition_size)).url
