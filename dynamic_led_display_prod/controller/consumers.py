from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.core import serializers
import base64
from .models import Programs,Elements,Panel
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
import secrets


class PorgramsAndElements(AsyncWebsocketConsumer):
    async def connect(self):        
        await self.accept()
    
    async def disconnect(self,close_code):        
        self.send(json.dumps(close_code))

    async def receive(self,text_data=None,bytes_data=None):        
        if text_data:
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
                    program_name = text_data.get('program_name')
                    element_name = text_data.get('element_name')
                    data = False
                    if element_name == 'text_element':
                        element_html = text_data.get('element_html')
                        data  = await self.add_element(program_name,element_name,element_html=element_html)
                
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
                
                if text_data['action'] == 'get_file_link':                    
                    element_name = text_data.get('element_name')
                    if element_name == 'image_element' and text_data.get('base64file'):
                        file_data_b64 = text_data.get('base64file')
                        file_name = text_data.get('file_name')
                        file_type = text_data.get('file_type')
                        file_link = await self.get_file_link(file_data_b64,file_name,file_type)
                        if(file_link):
                            await self.send(json.dumps({
                                'action':'get_image_link',
                                'element_name':element_name,
                                'image_link':file_link
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

                if text_data['action'] == 'program_animation_changed' and text_data.get('selected_program') and text_data.get('new_animation'):
                    animation = text_data['new_animation']
                    selected_program = text_data['selected_program']
                    result = await self.update_program_animation(selected_program,animation)
                    if result:
                        elements = await self.get_program_elements(selected_program=selected_program)            
                        program_code = await self.get_program_code(text_data['selected_program'])
                        if elements:
                            await self.send(json.dumps({
                                'action':'get_elements',
                                'elements':elements,
                                'program_name':selected_program,
                                'program_code':program_code,
                                'animation':animation,
                                'error':False
                        }))            

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
    def update_program_animation(self,selected_program,animation):
        program_obj = Programs.objects.get(program_name=selected_program)
        if program_obj:
            program_obj.animation = animation
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
    def add_element(self,program_name,element_name,element_html=False,file_link=False):
        program_obj = Programs.objects.get(program_name=program_name)      
        if element_name == 'text_element' and element_name:
            element_obj = Elements(element_name=element_name,code=element_html)
        elif element_name == 'image_element':
            pass        
        try:
            element_obj.save()
            program_obj.elements.add(element_obj)
            return True            
        except Exception as e:            
            return False
        
    async def get_file_link(self,file_data,file_name,file_type):
        format, base64_data = file_data.split(";", 1)
        format = format.split(":")[1]
        base64_data = base64_data.split(",")[1]                    
        bytes_data= base64.b64decode(base64_data)
        file_storage_obj = FileSystemStorage()
        file = ContentFile(bytes_data)
        random_prefix = secrets.token_hex(16)
        saved_file = file_storage_obj.save(f"{random_prefix}_{file_name}_{file_type.split('/')[1]}", file)
        file_url = file_storage_obj.url(saved_file)
        return file_url

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
        await self.handle_channel_join_leave_event('join',self.channel_name)
    
    async def disconnect(self,close_code):        
        self.send(json.dumps(close_code))
        await self.handle_channel_join_leave_event('leave',self.channel_name)

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
                if text_data['action'] == 'update_program' and text_data.get('program_code'):
                    await self.update_program(text_data['selected_program'],text_data['program_code'])

            if text_data['page'] == 'consumer':
                if text_data['action'] == 'connection':
                    PanelChangedConsumer.entities['consumer'] = self
                    await self.send(json.dumps({
                        'action':'connected'                        
                    }))
                if text_data['action'] == 'get_panel_configs':                    
                    program_data = await self.get_panel_configs()
                    await self.send(json.dumps({
                        'action':'configs_changed',
                        'program_data':program_data
                    }))

    async def program_event(self,event):  
        if PanelChangedConsumer.entities['consumer']:
            program_data = await PanelChangedConsumer.entities['consumer'].get_panel_configs()        
            await PanelChangedConsumer.entities['consumer'].send(json.dumps({
                        'action':'configs_changed',
                        'program_data':program_data
            }))
    @database_sync_to_async
    def handle_channel_join_leave_event(self,action,channel_name):
        panel_obj = Panel.objects.first()
        if panel_obj:
            if action == 'join':
                panel_obj.channel_name = channel_name
            else:
                panel_obj.channel_name = None
            panel_obj.save()
        
    @database_sync_to_async
    def update_program(self,selected_program,program_code):
        program = Programs.objects.get(program_name=selected_program)
        if program:
            program.panel_code = program_code
            program.save()
            return True
        else:
            return False
    @database_sync_to_async
    def get_panel_configs(self):
        panel_obj = Panel.objects.first()
        programs = panel_obj.return_program_in_order()
        if programs:
            programs_data = serializers.serialize('json', programs)
            return programs_data      
    
    @database_sync_to_async
    def set_new_sequence(self,sequence):
        obj = Panel.objects.first()
        if obj:
            obj.sequence = json.dumps(sequence)
            obj.save()
            return True
        else:
            return False