
class ExportParams(object):
    current_time = 0
    domain_url = ''
    models_path  = 'generated/'

    default_user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.122 Mobile Safari/537.36"

    @staticmethod
    def get_url(url):
        if url == '' or url.startswith('http://') or url.startswith('https://') or url.startswith('file://'):
            return url
        return ExportParams.domain_url + url
