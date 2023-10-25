from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.core import serializers
from .models import Programs,Elements,Panel


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
                program_code = await self.get_program_code(text_data['selected_program'])
                if elements:
                    await self.send(json.dumps({
                        'action':'get_elements',
                        'elements':elements,
                        'program_name':text_data['selected_program'],
                        'program_code':program_code,
                        'error':False
                        }))
                else:
                    await self.send(json.dumps({'action':'get_elements','error':False,'elements':None}))
            if text_data['action'] == 'add_program' and text_data.get('program_name'):
                result = await self.add_new_program(text_data['program_name'],code=text_data['code'])
                if result == True:
                    # await self.send(json.dumps({
                    #     'action':'add_program',
                    #     'message':text_data['program_name'],
                    #     'error':False
                    # }))
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
                    program_code = await self.get_program_code(text_data['selected_program'])
                    if elements:
                        await self.send(json.dumps({
                            'action':'get_elements',
                            'elements':elements,
                            'program_name':program_name,
                            'program_code':program_code,
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

            if text_data['action'] == 'update_element' and text_data.get('element_id') and text_data.get('element_code'):
                result  = await self.update_element(text_data['element_id'],text_data['element_code'])
                program_name = text_data['selected_program']
                if result == True:
                    elements = await self.get_program_elements(selected_program=program_name)            
                    program_code = await self.get_program_code(text_data['selected_program'])
                    if elements:
                        await self.send(json.dumps({
                            'action':'get_elements',
                            'elements':elements,
                            'program_name':program_name,
                            'program_code':program_code,
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

            if text_data['action'] == 'program_sequence_changed' and text_data.get('selected_program') and text_data.get('new_running_time'):
                new_running_time = text_data['new_running_time']
                selected_program = text_data['selected_program']
                await self.update_program_running_time(selected_program,new_running_time)                
        print('PorgramsAndElements',text_data)

    @database_sync_to_async
    def update_program_running_time(self,selected_program,new_running_time):
        program_obj = Programs.objects.get(program_name=selected_program)
        if program_obj:
            program_obj.running_time = new_running_time
            program_obj.save()
            return True
        else:
            return False
        
    @database_sync_to_async
    def update_element(self,element_id,element_code):
        element_obj = Elements.objects.get(pk=element_id)
        try:
            element_obj.code = element_code
            element_obj.save()
            return True
        except Exception as e:
            print(e)
            return False
        
    @database_sync_to_async
    def get_program_elements(self,selected_program):        
        program = Programs.objects.get(program_name=selected_program)
        if program:
            program_elements = program.elements.all()
            data = serializers.serialize('json', program_elements)
            return data
        return False
    @database_sync_to_async
    def get_program_code(self,selected_program):
        program = Programs.objects.get(program_name=selected_program)
        if program:
            return program.code
        else:
            return False
    @database_sync_to_async
    def get_active_programs(self):
        panel_obj = Panel.objects.first()
        programs = panel_obj.return_program_in_order()
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
    def add_new_program(self,program_name,code):
        program_obj = Programs(program_name=program_name,code=code)
        panel_obj = Panel.objects.first()
        try:
            program_obj.save()            
            panel_obj.programs.add(program_obj)            
            panel_obj.save()
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
    
class PanelChangedConsumer(AsyncWebsocketConsumer):
    entities = {
        'controller':None,
        'consumer':None
    }
    async def connect(self):        
        await self.accept()
    
    async def disconnect(self,close_code):        
        self.send(json.dumps(close_code))

    async def receive(self,text_data):
        text_data = json.loads(text_data)
        print('PanelChangedConsumer',text_data)
        if text_data.get('page'):
            if text_data['page'] == 'controller':
                if text_data['action'] == 'connection':
                    PanelChangedConsumer.entities['controller'] = self     
                if text_data['action'] == 'sequence_changed' and text_data.get('sequence'):
                    result = await self.set_new_sequence(text_data['sequence'])
                    if result:
                        pass
                    else:
                        pass

            if text_data['page'] == 'consumer':
                pass
    
    @database_sync_to_async
    def set_new_sequence(self,sequence):
        obj = Panel.objects.first()
        if obj:
            obj.sequence = json.dumps(sequence)
            obj.save()
            return True
        else:
            return False