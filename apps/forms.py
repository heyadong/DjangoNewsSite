class FormsMxin(object):
    def get_errors(self):
        if hasattr(self,'errors'):
            # {'username': [{'message': 'Enter a valid URL.', 'code': 'invalid'},
            # {'message': 'Ensure this value has at most 4 characters (it has 22).', 'code': 'max_length'}]}
            errors = self.errors.get_json_data()
            new_errors = {}
            for key, message_dicts in errors.items():
                messages = []
                for message in message_dicts:
                    messages.append(message['message'])
                new_errors[key] = messages
            return new_errors
        else:
            return {}