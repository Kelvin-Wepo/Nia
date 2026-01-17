import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()


class CoachingConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time coaching sessions.
    """
    
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = f'coaching_{self.session_id}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Receive message from WebSocket"""
        data = json.loads(text_data)
        message_type = data.get('type', 'message')
        
        if message_type == 'message':
            # Handle user message
            await self.handle_user_message(data)
        elif message_type == 'typing':
            # Broadcast typing indicator
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_indicator',
                    'user': data.get('user'),
                    'is_typing': data.get('is_typing', False)
                }
            )
    
    async def handle_user_message(self, data):
        """Process user message and get AI response"""
        message = data.get('message', '')
        
        # Save message to database
        await self.save_message('user', message)
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'role': 'user',
                'message': message,
            }
        )
        
        # Generate AI response (this would call the AI service)
        # For now, we'll just echo back
        ai_response = f"AI Coach: I understand you said '{message}'. Let me help you with that."
        
        await self.save_message('assistant', ai_response)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'role': 'assistant',
                'message': ai_response,
            }
        )
    
    async def chat_message(self, event):
        """Send message to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'message',
            'role': event['role'],
            'message': event['message'],
        }))
    
    async def typing_indicator(self, event):
        """Send typing indicator to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user': event['user'],
            'is_typing': event['is_typing'],
        }))
    
    @database_sync_to_async
    def save_message(self, role, content):
        """Save message to database"""
        from .models import Message, CoachingSession
        
        try:
            session = CoachingSession.objects.get(id=self.session_id)
            Message.objects.create(
                session=session,
                role=role,
                content=content
            )
        except CoachingSession.DoesNotExist:
            pass
