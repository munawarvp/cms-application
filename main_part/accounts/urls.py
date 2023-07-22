from django.urls import path
from .views import (UserList, CreateUsers,AuthenticateUser, GetUserDetails, UpdateUserDetails, DeleteUser, CreateBlog, LikeBlog,
                    ListAllBlogs, GetBlogDetails, UpdateBlog, DeleteBlog, Dislike, GetBlogLikes)



urlpatterns = [
    path('create-user/', CreateUsers.as_view(), name='create-user'),
    path('login-user/', AuthenticateUser.as_view()),
    path('list-users/', UserList.as_view(), name='list-users'),
    path('user/<int:user_id>', GetUserDetails.as_view(), name='user'),
    path('update-user/<int:user_id>', UpdateUserDetails.as_view(), name='update-user'),
    path('delete-user/<int:user_id>', DeleteUser.as_view(), name='delete-user'),

    path('create-blog/', CreateBlog.as_view(), name='create-blog'),
    path('list-blogs/', ListAllBlogs.as_view(), name='list-blogs'),
    path('blog/<int:blog>', GetBlogDetails.as_view(), name='blog'),
    path('update-blog/<int:blog>', UpdateBlog.as_view(), name='update-blog'),
    path('delete-blog/<int:blog_id>', DeleteBlog.as_view(), name='delete-blog'),

    path('like-blog/', LikeBlog.as_view(), name='like-blog'),
    path('blog-likes/<int:blog_id>', GetBlogLikes.as_view(), name='blog-likes'),
    path('dislike/<int:blog_id>', Dislike.as_view(), name='dislike'),
]
