from django.urls import path


class CustomRouter:

    urls = []

    def __init__(self):

        self.urls = []

    def register(self, url, view, name=None):

        url = url if url[-1] == '/' else url+'/'

        view_ = view()

        action_list = view_.get_action_fun_list()

        self.urls += [

            path(url, view.as_view({                                 # bulk

                'get': 'bulk_get',
                'post': 'bulk_post_request',
                'patch': 'bulk_patch_request',
                'delete': 'bulk_delete_request',

            })),

            path(f'{url}<slug_field>/', view.as_view({

                'get': 'single_get',
                'patch': 'single_patch_request',
                'delete': 'single_delete_request',
            })),

            path(f'{url}c/', view.as_view({

                'post': 'single_post_request',
            }))

        ]

        # self.urls += [
        #
        #     path(f'{url}p/', view.as_view({
        #
        #         'post': 'request_handler'
        #
        #     })),
        #
        # ]

        for action_name, _ in action_list.items():

            self.urls += [

                path(f'{url}<slug>/{action_name}/', view.as_view({

                    'post': f'action_{action_name}'

                })),

            ]
