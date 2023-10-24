from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.core import serializers
from .models import Programs,Elements


class PorgramsAndElements(AsyncWebsocketConsumer):
    async def connect(self):
        print(self)
        await self.accept()
    
    async def disconnect(self,close_code):        
        self.send(json.dumps(close_code))

    async def receive(self,text_data):
        text_data = json.loads(text_data)
        if text_data.get('action'):
            if text_data['action'] == 'get_programs':
                programs = await self.get_active_programs()            
                if programs:
                    await self.send(json.dumps({
                        'action':'get_programs',
                        'programs':programs,
                        'error':False
                        }))
                else:
                    await self.send(json.dumps({'action':'get_programs','error':False,'programs':None}))
                    
            if text_data['action'] == 'get_elements' and text_data.get('selected_program'):
                elements = await self.get_program_elements(text_data['selected_program'])            
                if elements:
                    await self.send(json.dumps({
                        'action':'get_elements',
                        'elements':elements,
                        'program_name':text_data['selected_program'],
                        'error':False
                        }))
                else:
                    await self.send(json.dumps({'action':'get_elements','error':False,'elements':None}))
            if text_data['action'] == 'add_program' and text_data.get('program_name'):
                result = await self.add_new_program(text_data['program_name'])
                if result == True:
                    await self.send(json.dumps({
                        'action':'add_program',
                        'message':text_data['program_name'],
                        'error':False
                    }))
                else:
                    await self.send(json.dumps({
                        'action':'add_program',
                        'message':result,
                        'error':True
                    }))
            if text_data['action'] == 'add_element' and text_data.get('element_name'):                
                program_name = text_data['program_name']
                element_name = text_data['element_name']
                element_html = text_data['element_html']
                data  = await self.add_element(program_name,element_name,element_html)
                if data:
                    await self.send(json.dumps({
                        'action':'add_element',
                        'error':False,
                        'message':'Element added successfully'
                    }))
                    
                else:
                    await self.send(json.dumps({
                        'action':'add_element',
                        'error':True,
                        'message':'Something went wrong'
                    }))


            if text_data['action'] == 'delete_program' and text_data.get('program_name'):
                result  = await self.delete_program(text_data['program_name'])
                if result == True:
                    programs = await self.get_active_programs()            
                    if programs:
                        await self.send(json.dumps({
                            'action':'get_programs',
                            'programs':programs,
                            'error':False
                            }))
                    else:
                        await self.send(json.dumps({'action':'get_programs','error':False,'programs':None}))
                else:
                    await self.send(json.dumps({
                        'action':'delete_programs',
                        'message':result,
                        'error':True
                    }))
            if text_data['action'] == 'delete_element' and text_data.get('element_id') and text_data.get('selected_program'):
                result  = await self.delete_element(text_data['element_id'])
                program_name = text_data['selected_program']
                if result == True:
                    elements = await self.get_program_elements(selected_program=program_name)            
                    if elements:
                        await self.send(json.dumps({
                            'action':'get_elements',
                            'elements':elements,
                            'program_name':program_name,
                            'error':False
                            }))
                    else:
                        await self.send(json.dumps({'action':'get_elements','error':False,'elements':None}))
                else:
                    await self.send(json.dumps({
                        'action':'delete_elements',
                        'message':result,
                        'error':True
                    }))

        print(text_data)

    @database_sync_to_async
    def get_program_elements(self,selected_program):        
        program = Programs.objects.get(program_name=selected_program)
        if program:
            program_elements = program.elements.all()
            data = serializers.serialize('json', program_elements)
            return data
        return False
    
    @database_sync_to_async
    def get_active_programs(self):
        programs = Programs.objects.all()
        if programs:
            data = serializers.serialize('json', programs)
            return data        
        return False
        
    @database_sync_to_async
    def add_element(self,program_name,element_name,element_html):
        program_obj = Programs.objects.get(program_name=program_name)        
        element_obj = Elements(element_name=element_name,code=element_html)
        try:
            element_obj.save()
            program_obj.elements.add(element_obj)
            return True            
        except Exception as e:            
            return False

    @database_sync_to_async
    def add_new_program(self,program_name):
        program_obj = Programs(program_name=program_name)        
        try:
            program_obj.save()            
        except Exception as e:
            return str(e)
        return True
    
    @database_sync_to_async
    def delete_program(self,program_name):
        try:
            program_obj = Programs.objects.get(program_name=program_name)
            program_obj.delete()
        except Exception as e:
            return str(e)
        return True

    @database_sync_to_async
    def delete_element(self,element_id):
        try:
            element_obj = Elements.objects.get(pk=element_id)
            element_obj.delete()
        except Exception as e:
            return str(e)
        return True

            

    