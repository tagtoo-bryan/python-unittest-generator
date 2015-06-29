import mock
import unittest
import facebook

class Testfacebook(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        return

    def test_get_object(self):
        def side_effect(*args, **kwargs):
            if args == ["'GET'", "'https://graph.facebook.com/v2.2/post_id'"] and kwargs == {'files': 'None', 'data': 'None', 'params': "{'access_token': 'post_id'}", 'timeout': 'None'}:
                return <Response [400]>
            if args == ["'GET'", "'https://graph.facebook.com/v2.2/'"] and kwargs == {'files': 'None', 'params': "{'access_token': 'post_id', 'ids': 'p,o,s,t,_,i,d,s'}", 'data': 'None', 'timeout': 'None'}:
                return <Response [400]>
            if args == ["'POST'", "'https://graph.facebook.com/v2.2/me/feed'"] and kwargs == {'files': 'None', 'data': "{'picture': 'http://www.example.com/thumbnail.jpg', 'description': 'This is a longer description of the attachment', 'access_token': 'post_id', 'caption': 'Check out this example', 'link': 'http://www.example.com/', 'message': 'put message on the wall......', 'name': 'Link name'}", 'params': '{}', 'timeout': 'None'}:
                return <Response [400]>

        facebook.requests.request = mock.Mock(side_effect=side_effect)

        try:
            result = facebook.GraphAPI(access_token='your_token', version='2.2').get_object(id = 'post_id')
        except Exception as e:
            self.assertEqual(e.__class__.__name__, 'GraphAPIError')


        return

    def test_get_objects(self):
        def side_effect(*args, **kwargs):
            if args == ["'GET'", "'https://graph.facebook.com/v2.2/'"] and kwargs == {'files': 'None', 'data': 'None', 'params': "{'access_token': 'post_id', 'ids': 'p,o,s,t,_,i,d,s'}", 'timeout': 'None'}:
                return <Response [400]>
            if args == ["'POST'", "'https://graph.facebook.com/v2.2/me/feed'"] and kwargs == {'files': 'None', 'params': '{}', 'data': "{'picture': 'http://www.example.com/thumbnail.jpg', 'description': 'This is a longer description of the attachment', 'access_token': 'post_id', 'caption': 'Check out this example', 'link': 'http://www.example.com/', 'message': 'put message on the wall......', 'name': 'Link name'}", 'timeout': 'None'}:
                return <Response [400]>

        facebook.requests.request = mock.Mock(side_effect=side_effect)

        try:
            result = facebook.GraphAPI(access_token='your_token', version='2.2').get_object(ids = 'post_ids')
        except Exception as e:
            self.assertEqual(e.__class__.__name__, 'GraphAPIError')


        return

    def test_put_wall_post(self):
        def side_effect(*args, **kwargs):
            if args == ["'POST'", "'https://graph.facebook.com/v2.2/me/feed'"] and kwargs == {'files': 'None', 'data': "{'picture': 'http://www.example.com/thumbnail.jpg', 'description': 'This is a longer description of the attachment', 'access_token': 'post_id', 'caption': 'Check out this example', 'link': 'http://www.example.com/', 'message': 'put message on the wall......', 'name': 'Link name'}", 'params': '{}', 'timeout': 'None'}:
                return <Response [400]>

        facebook.requests.request = mock.Mock(side_effect=side_effect)

        try:
            result = facebook.GraphAPI(access_token='your_token', version='2.2').get_object(message = 'put message on the wall......', attachment = {'caption': 'Check out this example', 'description': 'This is a longer description of the attachment', 'link': 'http://www.example.com/', 'name': 'Link name', 'picture': 'http://www.example.com/thumbnail.jpg'})
        except Exception as e:
            self.assertEqual(e.__class__.__name__, 'GraphAPIError')


        return




if __name__ == '__main__':
    unittest.main()