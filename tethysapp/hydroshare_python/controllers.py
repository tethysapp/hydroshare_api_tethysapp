from django.shortcuts import render
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import Button
from tethys_sdk.gizmos import TextInput, DatePicker, SelectInput
from tethys_sdk.gizmos import DataTableView
from tethys_services.backends.hs_restclient_helper import get_oauth_hs
from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.http import HttpResponse
from hs_restclient import HydroShare, HydroShareAuthBasic
from django.utils.encoding import smart_str
import os
import tempfile
import zipfile



@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    save_button = Button(
        display_text='',
        name='save-button',
        icon='glyphicon glyphicon-floppy-disk',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Save'
        }
    )

    edit_button = Button(
        display_text='',
        name='edit-button',
        icon='glyphicon glyphicon-edit',
        style='warning',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Edit'
        }
    )

    remove_button = Button(
        display_text='',
        name='remove-button',
        icon='glyphicon glyphicon-remove',
        style='danger',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Remove'
        }
    )

    previous_button = Button(
        display_text='Previous',
        name='previous-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Previous'
        }
    )

    next_button = Button(
        display_text='Next',
        name='next-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Next'
        }
    )

    context = {
        'save_button': save_button,
        'edit_button': edit_button,
        'remove_button': remove_button,
        'previous_button': previous_button,
        'next_button': next_button
    }

    return render(request, 'hydroshare_python/about.html', context)

@login_required()
def about(request):
    """
    Controller for the app home page.
    """
    save_button = Button(
        display_text='',
        name='save-button',
        icon='glyphicon glyphicon-floppy-disk',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Save'
        }
    )

    edit_button = Button(
        display_text='',
        name='edit-button',
        icon='glyphicon glyphicon-edit',
        style='warning',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Edit'
        }
    )

    remove_button = Button(
        display_text='',
        name='remove-button',
        icon='glyphicon glyphicon-remove',
        style='danger',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Remove'
        }
    )

    previous_button = Button(
        display_text='Previous',
        name='previous-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Previous'
        }
    )

    next_button = Button(
        display_text='Next',
        name='next-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Next'
        }
    ) 

    context = {
        'save_button': save_button,
        'edit_button': edit_button,
        'remove_button': remove_button,
        'previous_button': previous_button,
        'next_button': next_button
    }

    return render(request, 'hydroshare_python/about.html', context)

@login_required()
def get_file(request):
    """
    Controller for the Add Dam page.
    """
    # Default Values
    title = ''
    owner = 'Reclamation'
    username = ''
    password = ''
    # river = ''
    date_built = ''
    author = ''
    

    # Errors
    title_error = ''
    owner_error = ''
    username_error = ''
    password_error = ''
    # river_error = ''
    date_error = ''
    author_error = ''


    # Handle form submission
    if request.POST and 'create-button' in request.POST:
        # Get values
        has_errors = False
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        owner = request.POST.get('owner', None)
        # river = request.POST.get('river', None)
        date_built = request.POST.get('date-built', None)
        author = request.POST.get('author', None)
        coauthor = author.split(',')
        authorsObj = ""
        for i, author in enumerate(coauthor):
            separator = ',' if i>0 else ''
            authorsObj = authorsObj + separator + '{"creator":{"name":"'+author.strip()+'"}}'
        title = request.POST.get('title', None)
        print(dict(request.FILES))
        uploaded_file = request.FILES['uploadedfile']
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_zip_path = os.path.join(temp_dir, uploaded_file.name)
            print(temp_zip_path)

            # Use with statements to ensure opened files are closed when done
            with open(temp_zip_path, 'wb') as temp_zip:
                for chunk in uploaded_file.chunks():
                    temp_zip.write(chunk)

            # Validate
            if not title:
                has_errors = True
                title_error = 'Title is required.'

            if not owner:
                has_errors = True
                owner_error = 'Owner is required.'
            
            if not username:
                has_errors = True
                username_error = 'Username is required.'
            
            if not password:
                has_errors = True
                password_error = 'Password is required.'


            if not date_built:
                has_errors = True
                date_error = 'Date Built is required.'

            if not author:
                has_errors = True
                river_error = 'Author is required.'

            if not has_errors:
                # Do stuff here
                auth = HydroShareAuthBasic(username= username, password= password)
                hs = HydroShare(auth=auth)
                # hs.setAccessRules(public=True)
                abstract = date_built
                keywords = owner.split(', ')
                rtype = 'GenericResource'
                fpath = temp_zip_path #fpath = 'tethysapp/geocode/workspaces/app_workspace/output.txt'
                metadata = '[{"coverage":{"type":"period", "value":{"start":"01/01/2000", "end":"12/12/2010"}}}, '+authorsObj+']'
                extra_metadata = '{"key-1": "value-1", "key-2": "value-2"}'
                resource_id = hs.createResource(rtype, title, resource_file=fpath, keywords=keywords, abstract=abstract, metadata=metadata, extra_metadata=extra_metadata)
                messages.error(request, "Resource created successfully")
                # return {"status": success }
            if has_errors:    
            #Utah Municipal resource id
                messages.error(request, "Please fix errors.")

    # Define form gizmos
    title_input = TextInput(
        display_text='Title',
        name='title',
        placeholder= 'Enter the name of your resource'
    )

    owner_input = TextInput(
        display_text='Keywords',
        name='owner',
        placeholder='eg: shapefiles, datasets, etc..'
    )

    username_input = TextInput(
        display_text='Username',
        name='username',
        placeholder='Enter your username'
    )

    password_input = TextInput(
        display_text='Password',
        name='password',
        attributes={"type":"password"},
        placeholder='Enter your password'
    ) 

    # river_input = TextInput(
    #     display_text='Name of Creator',
    #     name='river',
    #     placeholder='e.g: John Smith'
    # )

    date_built = TextInput(
        display_text='Abstract',
        name='date-built',
        placeholder='Type in your abstract here'
    
    )

    author_input = TextInput(
        display_text='Creator/Creators',
        name='author',
        placeholder='Enter the name of the Owner and co-owners'
    )

    create_button = Button(
        display_text='Create',
        name='create-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        attributes={'form': 'add-dam-form'},
        submit=True
    )

    cancel_button = Button(
        display_text='Cancel',
        name='cancel-button',
        href=reverse('hydroshare_python:home')
    )

    context = {
        'title_input': title_input,
        'owner_input': owner_input,
        'username_input': username_input,
        'password_input': password_input,
        'date_built_input': date_built,
        'author_input': author_input,
        'create_button': create_button,
        'cancel_button': cancel_button,
    }

    return render(request, 'hydroshare_python/get_file.html', context)

@login_required()
def add_file(request):
    """
    Controller for the Add Dam page.
    """
    # Default Values
    username = ''
    password = ''
    # filename = ''
    resourcein = ''
    # owner = 'Reclamation'
    # river = ''
    # date_built = ''

    # Errors
    username_error = ''
    password_error = ''
    # filename_error = ''
    resourcein_error = ''
    # owner_error = ''
    # river_error = ''
    # date_error = ''

    # Handle form submission
    if request.POST and 'add-button' in request.POST:
        # Get values
        has_errors = False
        # filename = request.POST.get('filename', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        resourcein = request.POST.get('resourcein', None)
        print(dict(request.FILES))
        uploaded_file = request.FILES['addfile']

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_zip_path = os.path.join(temp_dir, uploaded_file.name)
            print(temp_zip_path)

            # Use with statements to ensure opened files are closed when done
            with open(temp_zip_path, 'wb') as temp_zip:
                for chunk in uploaded_file.chunks():
                    temp_zip.write(chunk)

            # Validate
            if not username:
                has_errors = True
                username_error = 'Username is required.'
        
            if not password:
                has_errors = True
                password_error = 'Password is required.'
            
            if not resourcein:
                has_errors = True
                resourcein_error = 'Resource is required.'

            # if not filename:
            #     has_errors = True
            #     filename_error = 'Filename is required.'

            if not has_errors:
                # Do stuff here
                # title = title
                # filename = filename
                auth = HydroShareAuthBasic(username= username, password= password)
                hs = HydroShare(auth=auth)
                fpath = temp_zip_path #'/Users/abu/Desktop/resources/nyu_2451_34514.shp.zip'
                resource_id = hs.addResourceFile(resourcein, fpath) #"remove_original_after_zip": True
                messages.error(request, "File added successfully")
                # return {"status": success }
            if has_errors:    
            #Utah Municipal resource id
                messages.error(request, "Please fix errors.")

    # Define form gizmos
    resourcein_input = TextInput(
        display_text='Resource ID',
        name='resourcein',
        placeholder='Enter id here eg: 08c6e88adaa647cd9bb28e5d619178e0 '
    )

    username_input = TextInput(
        display_text='Username',
        name='username',
        placeholder='Enter your username'
    )

    password_input = TextInput(
        display_text='Password',
        name='password',
        attributes={"type":"password"},
        placeholder='Enter your password'
    ) 

    # filename_input = TextInput(
    #     display_text='File name',
    #     name='title',
    #     placeholder='Enter the name of file here '
    # )

    # owner_input = TextInput(
    #     display_text='Keywords',
    #     name='owner',
    #     placeholder='eg: shapefiles, datasets, etc..'
    # ) 

    # river_input = TextInput(
    #     display_text='Name of Creator',
    #     name='river',
    #     placeholder='e.g: John Smith'
    # )

    # date_built = TextInput(
    #     display_text='Keywords',
    #     name='date-built',
    #     placeholder='e.g: Shapefiles, datasets, etc..'
    
    # )

    add_button = Button(
        display_text='Add',
        name='add-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        attributes={'form': 'add-dam-form'},
        submit=True
    )

    cancel_button = Button(
        display_text='Cancel',
        name='cancel-button',
        href=reverse('hydroshare_python:home')
    )

    context = {
        'resourcein_input': resourcein_input,
        'username_input': username_input,
        'password_input': password_input,
        # 'filename_input': filename_input,
        # 'owner_input': owner_input,
        # 'river_input': river_input,
        # 'date_built_input': date_built,
        'add_button': add_button,
        'cancel_button': cancel_button,
    }

    return render(request, 'hydroshare_python/add_file.html', context)

@login_required()
def delete_resource(request):
    """
    Controller for the Add Dam page.
    """
    # Default Values
    username = ''
    password = ''
    # filename = ''
    resourcein = ''
    # owner = 'Reclamation'
    # river = ''
    # date_built = ''

    # Errors
    username_error = ''
    password_error = ''
    # filename_error = ''
    resourcein_error = ''
    # owner_error = ''
    # river_error = ''
    # date_error = ''

    # Handle form submission
    if request.POST and 'delete-button' in request.POST:
        # Get values
        has_errors = False
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        resourcein = request.POST.get('resourcein', None)
        

        # Validate

        if not resourcein:
            has_errors = True
            resourcein_error = 'Resource ID is required.'
        
        if not username:
            has_errors = True
            username_error = 'Username is required.'
        
        if not password:
            has_errors = True
            password_error = 'Password is required.'

        # if not river:
        #     has_errors = True
        #     river_error = 'River is required.'



        if not has_errors:
            # Do stuff here
            auth = HydroShareAuthBasic(username= username, password= password)
            hs = HydroShare(auth=auth)
            hs.deleteResource(resourcein)
            messages.error(request, "Resource deleted successfully")
        if has_errors:    
            #Utah Municipal resource id
            messages.error(request, "Please fix errors.")

        

    # Define form gizmos
    resourcein_input = TextInput(
        display_text='Resource ID',
        name='resourcein',
        placeholder='Enter the Resource ID here'
    )

    username_input = TextInput(
        display_text='Username',
        name='username',
        placeholder='Enter your username'
    )

    password_input = TextInput(
        display_text='Password',
        name='password',
        attributes={"type":"password"},
        placeholder='Enter your password'
    ) 


    delete_button = Button(
        display_text='Delete Resource',
        name='delete-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        attributes={'form': 'add-dam-form'},
        submit=True
    )

    cancel_button = Button(
        display_text='Cancel',
        name='cancel-button',
        href=reverse('hydroshare_python:home')
    )

    context = {
        'resourcein_input': resourcein_input,
        'username_input': username_input,
        'password_input': password_input,
        'delete_button': delete_button,
        'cancel_button': cancel_button

    }

    return render(request, 'hydroshare_python/delete_resource.html', context)

@login_required()
def filev(request):
    """
    Controller for the Add Dam page.
    """
    # Default Values
    # filename = ''
    username = ''
    password = ''
    resourcein = ''
    # owner = 'Reclamation'
    # river = ''
    # date_built = ''

    # Errors
    title_error = ''
    # filename_error = ''
    resourcein_error = ''
    username_error = ''
    password_error = ''
    # date_error = ''

    # Handle form submission
    if request.POST:
        # Get values
        has_errors = False
        # filename = request.POST.get('filename', None)
        resourcein = request.POST.get('resourcein', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        
        # Validate

        if not resourcein:
            has_errors = True
            resourcein_error = 'Resource ID is required.'
        
        if not username:
            has_errors = True
            username_error = 'Username is required.'
        
        if not password:
            has_errors = True
            password_error = 'Password is required.'

        # if not river:
        #     has_errors = True
        #     river_error = 'River is required.'

        if not has_errors:
            # Do stuff here
            auth = HydroShareAuthBasic(username= username, password= password)
            hs = HydroShare(auth=auth)
            resourcefiles=hs.resource(resourcein).files.all().content
            return HttpResponse(resourcefiles)

        return HttpResponse('')
           
@login_required()
def delete_file(request):
    """
    Controller for the Add Dam page.
    """
    # Default Values
    title = ''
    # filename = ''
    username = ''
    password = ''
    resourcein = ''
    filev = []
    # owner = 'Reclamation'
    # river = ''
    # date_built = ''

    # Errors
    title_error = ''
    # filename_error = ''
    resourcein_error = ''
    username_error = ''
    password_error = ''
    # date_error = ''

    # Handle form submission
    if request.POST and 'delete-button' in request.POST:
        # Get values
        has_errors = False
        # filename = request.POST.get('filename', None)
        resourcein = request.POST.get('resourcein', None)
        title = request.POST.get('title_input', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        

        # Validate

        if not resourcein:
            has_errors = True
            resourcein_error = 'Resource ID is required.'

        
        if not username:
            has_errors = True
            username_error = 'Username is required.'
        
        if not password:
            has_errors = True
            password_error = 'Password is required.'

        # if not river:
        #     has_errors = True
        #     river_error = 'River is required.'

        if not has_errors:
            # Do stuff here
            auth = HydroShareAuthBasic(username= username, password= password)
            hs = HydroShare(auth=auth)
            resource_id = hs.deleteResourceFile(resourcein, title)
            messages.error(request, "File deleted successfully")
        if has_errors:    
                #Utah Municipal resource id
            messages.error(request, "Please fix errors.")

        

    # Define form gizmos
    resourcein_input = TextInput(
        display_text='Resource ID',
        name='resourcein',
        placeholder='Enter the Resource ID here'
    )


    username_input = TextInput(
        display_text='Username',
        name='username',
        placeholder='Enter your username'
    )

    password_input = TextInput(
        display_text='Password',
        name='password',
        attributes={"type":"password"},
        placeholder='Enter your password'
    ) 


    delete_button = Button(
        display_text='Delete File',
        name='delete-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        attributes={'form': 'add-dam-form'},
        submit=True
    )

    cancel_button = Button(
        display_text='Cancel',
        name='cancel-button',
        href=reverse('hydroshare_python:home')
    )

    context = {
        'resourcein_input': resourcein_input,
        'username_input': username_input,
        'password_input': password_input,
        'delete_button': delete_button,
        'cancel_button': cancel_button,
        'filev': filev

    }

    return render(request, 'hydroshare_python/delete_file.html', context)

@login_required()
def find_resource(request):
    """
    Controller for the Add Dam page.
    """
    # Default Values
    username = ''
    password = ''
    resourcesv = []

    # Errors
    username_error = ''
    password_error = ''

    # Handle form submission
    if request.POST and 'add-button' in request.POST:
        # Get values
        has_errors = False
        # filename = request.POST.get('filename', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        # Validate

        if not username:
            has_errors = True
            username_error = 'Username is required.'
    
        if not password:
            has_errors = True
            password_error = 'Password is required.'
        
        if has_errors:
            messages.error(request, "Please fix errors.")

        if not has_errors:
            auth = HydroShareAuthBasic(username= username, password= password)
            hs = HydroShare(auth=auth)
            for resource in hs.resources():
                print(resource)
                resourcesv.append(resource)
        #Utah Municipal resource id

    # Define form gizmos

    username_input = TextInput(
        display_text='Username',
        name='username',
        placeholder='Enter your username'
    )

    password_input = TextInput(
        display_text='Password',
        name='password',
        placeholder='Enter your password'
    )

    add_button = Button(
        display_text='Add',
        name='add-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        attributes={'form': 'add-dam-form'},
        submit=True
    )

    cancel_button = Button(
        display_text='Cancel',
        name='cancel-button',
        href=reverse('hydroshare_python:home')
    )

    context = {
        'username_input': username_input,
        'password_input': password_input,
        'add_button': add_button,
        'cancel_button': cancel_button,
        'resourcesv' : resourcesv
    }

    return render(request, 'hydroshare_python/find_resource.html', context)

@login_required()
def download_file(request):
    """
    Controller for the Add Dam page.
    """
    # Default Values
    title = ''
    # filename = ''
    username = ''
    password = ''
    resourcein = ''
    # owner = 'Reclamation'
    # river = ''
    # date_built = ''

    # Errors
    title_error = ''
    # filename_error = ''
    resourcein_error = ''
    username_error = ''
    password_error = ''
    # date_error = ''

    # Handle form submission
    if request.POST and 'add-button' in request.POST:
        # Get values
        has_errors = False
        # filename = request.POST.get('filename', None)
        resourcein = request.POST.get('resourcein', None)
        title = request.POST.get('title', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        

        # Validate

        if not resourcein:
            has_errors = True
            resourcein_error = 'Resource ID is required.'

        if not title:
            has_errors = True
            title_error = 'Title is required.'
        
        if not username:
            has_errors = True
            username_error = 'Username is required.'
        
        if not password:
            has_errors = True
            password_error = 'Password is required.'

        # if not river:
        #     has_errors = True
        #     river_error = 'River is required.'

        if not has_errors:
            # Do stuff here
            auth = HydroShareAuthBasic(username= username, password= password)
            hs = HydroShare(auth=auth)
            fname = title
            fpath = hs.getResourceFile(resourcein, fname, destination= '/tmp')
            

            response = HttpResponse( content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(fname)

            response['X-Sendfile'] = smart_str('/tmp')
# It's usually a good idea to set the 'Content-Length' header too.
# You can also set any other required headers: Cache-Control, etc.
            messages.error(request, "File downloaded succesfully")
            return response
        messages.error(request, "Please fix errors.")

    # Define form gizmos
    resourcein_input = TextInput(
        display_text='Resource ID',
        name='resourcein'
    )

    title_input = TextInput(
        display_text='Name of the file you want to download including the extension',
        name='title',
        placeholder='eg: filename.shp or filename.txt'
    )

    username_input = TextInput(
        display_text='Username',
        name='username',
        placeholder='Enter your username'
    )

    password_input = TextInput(
        display_text='Password',
        name='password',
        placeholder='Enter your password'
    ) 


    add_button = Button(
        display_text='Add',
        name='add-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        attributes={'form': 'add-dam-form'},
        submit=True
    )

    cancel_button = Button(
        display_text='Cancel',
        name='cancel-button',
        href=reverse('hydroshare_python:home')
    )

    context = {
        'resourcein_input': resourcein_input,
        'title_input': title_input,
        'username_input': username_input,
        'password_input': password_input,
        'add_button': add_button,
        'cancel_button': cancel_button

    }

    return render(request, 'hydroshare_python/download_file.html', context)