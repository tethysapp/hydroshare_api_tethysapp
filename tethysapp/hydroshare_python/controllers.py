from django.shortcuts import render
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import Button
from tethys_sdk.gizmos import TextInput, DatePicker, SelectInput
from tethys_sdk.gizmos import DataTableView
# from .model import get_all_dams
from django.shortcuts import redirect, reverse
from django.contrib import messages
from hs_restclient import HydroShare, HydroShareAuthBasic
import os
import tempfile
import zipfile


auth = HydroShareAuthBasic(username='abhishekamal18@gmail.com', password='hydro1234')
hs = HydroShare(auth=auth)

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

    return render(request, 'hydroshare_python/home.html', context)

   

@login_required()
def get_file(request):
    """
    Controller for the Add Dam page.
    """
    # Default Values
    title = ''
    owner = 'Reclamation'
    # river = ''
    date_built = ''
    author = ''
    coauthor = ''

    # Errors
    title_error = ''
    owner_error = ''
    # river_error = ''
    date_error = ''
    author_error = ''
    coauthor_error = ''


    # Handle form submission
    if request.POST and 'add-button' in request.POST:
        # Get values
        has_errors = False
        title = request.POST.get('title', None)
        owner = request.POST.get('owner', None)
        # river = request.POST.get('river', None)
        date_built = request.POST.get('date-built', None)
        author = request.POST.get('author', None)
        coauthor = request.POST.get('coauthor', None)
        

        # Validate
        if not title:
            has_errors = True
            title_error = 'Title is required.'

        if not owner:
            has_errors = True
            owner_error = 'Owner is required.'

        # if not river:
        #     has_errors = True
        #     river_error = 'River is required.'

        if not date_built:
            has_errors = True
            date_error = 'Date Built is required.'

        if not author:
            has_errors = True
            river_error = 'Author is required.'

        if not coauthor:
            has_errors = True
            date_error = 'Author is required.'

        if not has_errors:
            # Do stuff here
            abstract = date_built
            keywords = owner.split(', ')
            rtype = 'GenericResource'
            fpath = '/Users/abu/Desktop/resources/tl_2017_06059_roads.shp' #fpath = 'tethysapp/geocode/workspaces/app_workspace/output.txt'
            metadata = '[{"coverage":{"type":"period", "value":{"start":"01/01/2000", "end":"12/12/2010"}}}, {"creator":{"name":"'+author+'"}}, {"creator":{"name":"'+coauthor+'"}}]'
            extra_metadata = '{"key-1": "value-1", "key-2": "value-2"}'
            resource_id = hs.createResource(rtype, title, resource_file=fpath, keywords=keywords, abstract=abstract, metadata=metadata, extra_metadata=extra_metadata)
            return redirect(reverse('hydroshare_python:home'))

        messages.error(request, "Please fix errors.")

    # Define form gizmos
    title_input = TextInput(
        display_text='Title',
        name='title'
    )

    owner_input = TextInput(
        display_text='Keywords',
        name='owner',
        placeholder='eg: shapefiles, datasets, etc..'
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
        display_text='author',
        name='author'
    )

    coauthor_input = TextInput(
        display_text='coauthor',
        name='coauthor'
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
        'title_input': title_input,
        'owner_input': owner_input,
        # 'river_input': river_input,
        'date_built_input': date_built,
        'author_input': author_input,
        'coauthor_input': coauthor_input,
        'add_button': add_button,
        'cancel_button': cancel_button,
    }

    return render(request, 'hydroshare_python/get_file.html', context)

@login_required()
def add_file(request):
    """
    Controller for the Add Dam page.
    """
    # Default Values
    title = ''
    # filename = ''
    resourcein = ''
    # owner = 'Reclamation'
    # river = ''
    # date_built = ''

    # Errors
    title_error = ''
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
        resourcein = request.POST.get('resourcein', None)
        title = request.POST.get('title', None)
        print(dict(request.FILES))
        uploaded_file = request.FILES['addfile']

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_zip_path = os.path.join(temp_dir, title+'.shp')
            print(temp_zip_path)

            # Use with statements to ensure opened files are closed when done
            with open(temp_zip_path, 'wb') as temp_zip:
                for chunk in uploaded_file.chunks():
                    temp_zip.write(chunk)

            # Validate
            if not title:
                has_errors = True
                title_error = 'Title is required.'
            
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
                fpath = temp_zip_path #'/Users/abu/Desktop/resources/nyu_2451_34514.shp.zip'
                resource_id = hs.addResourceFile(resourcein, fpath) #"remove_original_after_zip": True
                return redirect(reverse('hydroshare_python:home'))
            #Utah Municipal resource id
            messages.error(request, "Please fix errors.")

    # Define form gizmos
    title_input = TextInput(
        display_text='Title',
        name='title'
    )

    resourcein_input = TextInput(
        display_text='Resource ID',
        name='resourcein',
        placeholder='Enter id here eg: 08c6e88adaa647cd9bb28e5d619178e0 '
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
        'title_input': title_input,
        'resourcein_input': resourcein_input,
        # 'filename_input': filename_input,
        # 'owner_input': owner_input,
        # 'river_input': river_input,
        # 'date_built_input': date_built,
        'add_button': add_button,
        'cancel_button': cancel_button,
    }

    return render(request, 'hydroshare_python/add_file.html', context)

# @login_required()
# def delete_file(request):
#     """
#     Controller for the Add Dam page.
#     """
#     # Default Values
#     title = ''
#     # filename = ''
#     resourcein = ''
#     # owner = 'Reclamation'
#     # river = ''
#     # date_built = ''

#     # Errors
#     title_error = ''
#     # filename_error = ''
#     resourcein_error = ''
#     # owner_error = ''
#     # river_error = ''
#     # date_error = ''

#     # Handle form submission
#     if request.POST and 'add-button' in request.POST:
#         # Get values
#         has_errors = False
#         # filename = request.POST.get('filename', None)
#         resourcein = request.POST.get('resourcein', None)
#         title = request.POST.get('title', None)
#         print(dict(request.FILES))
#         uploaded_file = request.FILES['addfile']

#         with tempfile.TemporaryDirectory() as temp_dir:
#             temp_zip_path = os.path.join(temp_dir, title+'.shp')
#             print(temp_zip_path)

#             # Use with statements to ensure opened files are closed when done
#             with open(temp_zip_path, 'wb') as temp_zip:
#                 for chunk in uploaded_file.chunks():
#                     temp_zip.write(chunk)

#             # try:
#             #     # Extract the archive to the temporary directory
#             #     with zipfile.ZipFile(temp_zip_path) as temp_zip:
#             #         temp_zip.extractall(temp_dir)

#             # except zipfile.BadZipFile:
#             #     # Return error message
#             #     return 'You must provide a zip archive containing a shapefile.'

#             # owner = request.POST.get('owner', None)
#             # river = request.POST.get('river', None)
#             # date_built = request.POST.get('date-built', None)
#             # resource = request.POST.get('resource', None)
#             # filename = request.POST.get('filename', None)

#             # Validate
#             if not title:
#                 has_errors = True
#                 title_error = 'Title is required.'
            
#             if not resourcein:
#                 has_errors = True
#                 resourcein_error = 'Resource is required.'

#             # if not filename:
#             #     has_errors = True
#             #     filename_error = 'Filename is required.'

#             if not has_errors:
#                 # Do stuff here
#                 # title = title
#                 # filename = filename
#                 fpath = temp_zip_path #'/Users/abu/Desktop/resources/nyu_2451_34514.shp.zip'
#                 resource_id = hs.addResourceFile(resourcein, fpath) #"remove_original_after_zip": True
#                 return redirect(reverse('hydroshare_python:home'))
#             #Utah Municipal resource id
#             messages.error(request, "Please fix errors.")

#     # Define form gizmos
#     title_input = TextInput(
#         display_text='Title',
#         name='title'
#     )

#     resourcein_input = TextInput(
#         display_text='Resource ID',
#         name='resourcein',
#         placeholder='Enter id here eg: 08c6e88adaa647cd9bb28e5d619178e0 '
#     )

#     # filename_input = TextInput(
#     #     display_text='File name',
#     #     name='title',
#     #     placeholder='Enter the name of file here '
#     # )

#     # owner_input = TextInput(
#     #     display_text='Keywords',
#     #     name='owner',
#     #     placeholder='eg: shapefiles, datasets, etc..'
#     # ) 

#     # river_input = TextInput(
#     #     display_text='Name of Creator',
#     #     name='river',
#     #     placeholder='e.g: John Smith'
#     # )

#     # date_built = TextInput(
#     #     display_text='Keywords',
#     #     name='date-built',
#     #     placeholder='e.g: Shapefiles, datasets, etc..'
    
#     # )

#     add_button = Button(
#         display_text='Add',
#         name='add-button',
#         icon='glyphicon glyphicon-plus',
#         style='success',
#         attributes={'form': 'add-dam-form'},
#         submit=True
#     )

#     cancel_button = Button(
#         display_text='Cancel',
#         name='cancel-button',
#         href=reverse('hydroshare_python:home')
#     )

#     context = {
#         'title_input': title_input,
#         'resourcein_input': resourcein_input,
#         # 'filename_input': filename_input,
#         # 'owner_input': owner_input,
#         # 'river_input': river_input,
#         # 'date_built_input': date_built,
#         'add_button': add_button,
#         'cancel_button': cancel_button,
#     }

#     return render(request, 'hydroshare_python/delete_file.html', context)
