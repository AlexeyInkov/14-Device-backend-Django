class DataMixin:
    title_page = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context["title"] = self.title_page

    #
    # def get_mixin_context(self, context, **kwargs):
    #     context.update(kwargs)
    #     return context


# class CustomHtmxMixin:
#     def dispatch(self, request, *args, **kwargs):
#         # import pdb; pdb.set_trace()
#         self.template_htmx = self.template_name
#         if not self.request.META.get('HTTP_HX_REQUEST'):
#             self.template_name = 'components/include_block.html'
#         else:
#             time.sleep(1)
#         return super().dispatch(request, *args, **kwargs)
#     def get_context_data(self, **kwargs):
#         kwargs['template_htmx'] = self.template_htmx
#         return super().get_context_data(**kwargs)
