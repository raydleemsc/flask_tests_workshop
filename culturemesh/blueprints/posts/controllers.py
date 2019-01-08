from flask import Blueprint, render_template, request
from flask_login import current_user
from culturemesh.client import Client
from culturemesh.utils import get_time_ago
from culturemesh.utils import get_network_title
from culturemesh.utils import safe_get_query_arg

from culturemesh.blueprints.posts.forms.post_forms import *

from culturemesh.blueprints.posts.config import NUM_REPLIES_TO_SHOW


posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route("/", methods=['GET'])
def render_post():

    current_post_id = safe_get_query_arg(request, 'id')

    user_id = current_user.get_id()
    c = Client(mock=False)
    post = c.get_post(current_post_id)
    print('---------- c.get_post ----------')
    print(c.get_post(current_post_id))
    print('----------')

    post['network_title'] = get_network_title(c.get_network(post['id_network']))
    print("---------- c.get_network ----------")
    print(c.get_network(post['id_network']))
    print('----------')
    post['username'] = c.get_user(post["id_user"])["username"]
    print('---------- c.get_user ----------')
    print(c.get_user(post['id_user']))
    print('----------')
    post['time_ago'] = get_time_ago(post['post_date'])

    # NOTE: this will not show more than the latest 100 replies
    replies = c.get_post_replies(post["id"], NUM_REPLIES_TO_SHOW)
    print('---------- replies ----------')
    print(replies)
    print('----------')
    replies = sorted(replies, key=lambda x: int(x['id']))

    error_msg = None

    for reply in replies:
        reply['username'] = c.get_user(reply["id_user"])["username"]
        print('---------- c.get_user(reply) ----------')
        print(c.get_user(reply['id_user']))
        print('----------')
        reply['time_ago'] = get_time_ago(reply['reply_date'])

    new_form = CreatePostReplyForm()

    return render_template(
      'post.html',
      post=post,
      replies=replies,
      num_replies=len(replies),
      curr_user_id=user_id,
      form=new_form,
      error_msg=error_msg
    )
