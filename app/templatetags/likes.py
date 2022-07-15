from django import template

register = template.Library()

@register.filter(name='like_unlike')
def like_unlike(post,id):
   lk = post.like.all()
   for like in lk:
      if like.id == id:
         return False
   return True

@register.filter(name='total_like')
def total_like(t):
   lk = t.like.all()
   l = 0
   for like in lk:
      l = l+1
   return l




@register.filter(name='user_reply')
def user_reply(comment,reply):
   if comment==reply:
      return True
   else:
      return False


@register.filter(name='follow')
def follow(users,flo):
   f = users.user
   for i in flo:
      if i == f:
         return True
   return False
