from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model

User=get_user_model()

class ChatRoom(models.Model):
    user1 = models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name="user1")
    user2 = models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name="user2")

class Chat(models.Model):
    chatroom = models.ForeignKey(ChatRoom,null=True,related_name="chats",on_delete=models.CASCADE)
    sender = models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name="sender")
    reciever = models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name="reciever")
    message = models.TextField(null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False, blank=True, null=True)
      
    def __str__(self):
        return str(self.user)
